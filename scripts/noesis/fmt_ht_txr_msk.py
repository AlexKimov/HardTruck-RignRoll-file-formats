from inc_noesis import *
import os
#from timeit import default_timer as timer
from struct import unpack
#from math import floor
import noewin


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 1/2 Textures", ".msk;.txr")
    #noesis.logPopup()
    noesis.setHandlerTypeCheck(handle, htCheckType)
    noesis.setHandlerLoadRGBA(handle, htLoadRGBA)
    
    handle = noesis.register("Hard Truck 1/2 masks", ".msk")
    noesis.setHandlerWriteRGBA(handle, htMSKWriteRGBA)
    handle = noesis.register("Hard Truck 1/2 textures", ".txr")
    noesis.setHandlerWriteRGBA(handle, htTXRWriteRGBA)
 
    noesis.addOption(handle, "-htgame", "specify hard truck game (ht1, ht2)", \
        noesis.OPTFLAG_WANTARG) 
    noesis.addOption(handle, "-format", "pixel format (ht1, ht2)", \
        noesis.OPTFLAG_WANTARG) 
    noesis.addOption(handle, "-genmipmaps", "pixel format (ht1, ht2)", 0)        
    return 1

    
class HTImage:
    def __init__(self, reader):
        self.reader = reader
        self.extension = ""
        self.magic = 0 # 909202253 - "MS16", 1263747405 - "MASK"
        self.IDLength = 0
        self.bitDepth = 0
        self.imageWidth = 0
        self.imageHeight = 0
        self.bitsRed = 0
        self.bitsGreen = 0
        self.bitsBlue = 0
        self.bitsAlpha = 0
        self.bitMaskPos = 0
        self.imageSize = 0
    
    def readBitMask(self, filereader):
        pos = filereader.tell()
        
        filereader.seek(self.bitMaskPos, NOESEEK_ABS)
        
        filereader.seek(8, NOESEEK_REL)
        self.bitsRed = filereader.readUInt()
        self.bitsGreen = filereader.readUInt()
        self.bitsBlue = filereader.readUInt()
        self.bitsAlpha = filereader.readUInt()

        filereader.seek(pos, NOESEEK_ABS)        
    
    def readTXRHeader(self, filereader):
        # actually TGA header
        self.IDLength = filereader.readByte()
        
        filereader.seek(12, NOESEEK_ABS)
        
        self.imageWidth = filereader.readShort()
        self.imageHeight = filereader.readShort()
        
        self.bitDepth = filereader.readByte() / 8 # 1 - Hard Truck 1, 2 - HT 2
        
        filereader.seek(1, NOESEEK_REL)
        
        self.imageSize = self.imageWidth*self.imageHeight

        # trying to get bit masks position, what we need is "PFRM" section
        # masks are always at the end of file
        if self.IDLength > 0:
            filereader.seek(8, NOESEEK_REL)           
            self.bitMaskPos = filereader.readUInt() 
            
            # check if our section is "LVMP" not "PFRM" 
            if self.bitDepth == 2:              
                pos = filereader.tell()
                filereader.seek(self.bitMaskPos, NOESEEK_ABS)  
                           
                if filereader.readUInt() == 1347245644: # LVMP
                    size = filereader.readUInt()
                    self.bitMaskPos = self.bitMaskPos + size + 10
                
                filereader.seek(pos, NOESEEK_ABS)    
            return 0        
     
    def readMSKHeader(self, filereader):
        self.magic = filereader.readUInt() 
        
        self.imageWidth = filereader.readShort()
        self.imageHeight = filereader.readShort() 
        
        self.imageSize = self.imageWidth*self.imageHeight
      
        if self.magic == 909202253:                         
            self.bitMaskPos = filereader.getSize() - 44            
        return 0 
        
    def palettedToRGBA32(self, palBuffer, indBuffer):                 
        #imageData = bytearray()
        
        #palBuffer = memoryview(palBuffer)
        #alpha = memoryview(bytes([255]))
        
        #start = timer()  
        
        #for index in indBuffer:
        #    imageData += palBuffer[index*3 + 2]            
        #    imageData += palBuffer[index*3 + 1]
        #    imageData += palBuffer[index*3]            
        #    imageData += alpha[0]
            
        #end = timer()       
        #print(end - start)   
        #return imageData
               
        data = rapi.imageDecodeRawPal(indBuffer, palBuffer, self.imageWidth, \
            self.imageHeight, 8, "b8g8r8")
       
        return data         
                        
    def getPalettedImageFromFile(self, filereader):                 
        palBuffer = filereader.readBytes(768)       
        indBuffer = filereader.readBytes(self.imageSize)    
               
        return self.palettedToRGBA32(palBuffer, indBuffer) 
    
    def unpackRLEImageData(self, filereader):           
        unpackedImageData = bytearray(self.imageHeight * self.imageWidth * \
            self.bitDepth) 
               
        bufferPos = 0
        
        while filereader.tell() < self.bitMaskPos:
            controlFlag = filereader.readUByte()
            
            if controlFlag <= 127: 
                # raw data
                unpackedImageData[bufferPos: \
                        bufferPos + controlFlag*self.bitDepth] = \
                    filereader.readBytes(controlFlag*self.bitDepth)
                bufferPos += controlFlag*self.bitDepth
            else:  
                # packed pixels
                bufferPos += (controlFlag - 128)*self.bitDepth 
        
        return unpackedImageData
    
    def unpackRGBAImage(self, filereader):        
        # goto PFRM section to read bit masks
        #filereader.seek(self.bitMaskPos, NOESEEK_ABS)
        self.readBitMask(filereader)
        
        # return to RLE packed image data
        filereader.seek(768 + 8, NOESEEK_ABS) # 8 - header size
        
        imageBuffer = self.unpackRLEImageData(filereader)       

        return self.getRGBAImage(imageBuffer) 
        
    def unpackPalettedImage(self, filereader):
        # get palette
        palBuffer = filereader.readBytes(768)
        # get packed indexes
        #imageDataBuffer = filereader.getBuffer()[filereader.tell():]
      
        self.bitMaskPos = filereader.getSize()
        
        # unpack (RLE compression) palette indexes        
        indBuffer = self.unpackRLEImageData(filereader)
        
        return self.palettedToRGBA32(palBuffer, indBuffer)
    
    def getRGBAImage(self, imageBuffer):
    
        #buffer = unpack('H'*(len(imageBuffer)//2), imageBuffer)
    
        # bit unpack tables
        #table2 = [0, 255] 
        #table16 = bytes([0, 17, 34, 51, 68, 86, 102, 119, 136, 153, 170, 181, \
        #    204, 221, 238, 255])
        #table32 = bytes([0, 8, 16, 25, 33, 41, 49, 58, 66, 74, 82, 90, 99, \
        #    107, 115, 123, 132, 140, 148, 156, 165, 173, 181, 189, 197, 206, \
        #    214, 222, 230, 239, 247, 255])
        #table64 = bytes([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 49, 53, \
        #    57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, \
        #    117, 121, 125, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, \
        #    170, 174, 178, 182, 186, 190, 194, 198, 202, 206, 210, 215, 219, \
        #    223, 227, 231, 235, 239, 243, 247, 251, 255])   
 
        # speed up a little bit
        #table16 = memoryview(table16)
        #table32 = memoryview(table32)
        #table64 = memoryview(table64)
        
        #imageData = bytearray()  
        
        #unpack RGBA 16 bit to RGBA 32 bit       
        #for pixel in buffer:        
        #   if self.bitsRed == 63488: # RGB 565             
        #       imageData += table32[(pixel >> 11) & 31] 
        #       imageData += table64[(pixel >> 5) & 63] 
        #       imageData += table32[pixel & 31] 
        #       imageData += table32[31] # 255 - alpha               
        #   elif self.bitsRed == 31744: # RGB 5551          
        #       imageData += table32[(pixel >> 10) & 31] 
        #       imageData += table32[(pixel >> 5) & 31]               
        #       imageData += table32[pixel & 31]  
        #       imageData += table32[31]
        #   else: # RGBA 4444            
        #       imageData += table16[(pixel >> 8) & 15]  
        #       imageData += table16[(pixel >> 4) & 15]                
        #       imageData += table16[pixel & 15] 
        #       imageData += table16[(pixel >> 12) & 15]
               
        #if self.bitsRed == 63488: # BGR 565
        #    format = "b5g6r5"
        #elif self.bitsRed == 31744: # BGR 5551
        #    format = "b5g5r5a1"
        #else: # BGRA 4444 
        #    format = "b4g4r4a4"
        
        # all 16 bit RGBA formats: BGR565, BGRA5551, BGRA4444         
        formats = {63488:"b5g6r5", 31744:"b5g5r5a1", 3840:"b4g4r4a4"}         
        format = formats.get(self.bitsRed)      
            
        #noesis.logPopup()    
        #start = timer()   
        
        imageData = rapi.imageDecodeRaw(imageBuffer, self.imageWidth, \
            self.imageHeight, format)
                              
        if self.bitsRed == 31744: # change alpha component from 0 to 255 
            i = 0 
            size = len(imageData)         
            for i in range(size):
                if not(i & 3):            
                    imageData[i - 1] = 255   
                
        #end = timer() 
        #print(end - start)
        
        return imageData 
        
    def getRGBAImageFromFile(self, filereader):
        # get image from file
        imageBuffer = filereader.readBytes(self.imageSize*2)     
        
        self.readBitMask(filereader)  
        
        return self.getRGBAImage(imageBuffer)                
            
    def readTXRdata(self, filereader):
        if self.bitDepth == 1:
            return self.getPalettedImageFromFile(filereader)
        else:    
            return self.getRGBAImageFromFile(filereader)
       
    def readMSKdata(self, filereader):
        if self.magic == 909202253:
            self.bitDepth = 2
            return self.unpackRGBAImage(filereader)
        else: 
            self.bitDepth = 1        
            return self.unpackPalettedImage(filereader)    
    
    def getFileExtension(self):
        type = self.reader.readUByte()
        self.reader.seek(0, NOESEEK_ABS)
        return ".msk" if (type == 77) else ".txr"   
    
    def parseHeader(self):
        self.extension = self.getFileExtension()
        #noesis.logPopup()
        if self.extension == ".txr":
            if self.readTXRHeader(self.reader) == 1:
                return -1
        else: 
            if self.readMSKHeader(self.reader) == 1:
                return -1
        return 0
        
    def getData(self):      
        if self.extension == ".txr":
            return self.readTXRdata(self.reader)
        else:
            return self.readMSKdata(self.reader)             
	  
def htCheckType(data):
    htImage = HTImage(NoeBitStream(data))
    if htImage.parseHeader() != 0:
        return 0
    return 1

    
def htLoadRGBA(data, texList):
    htImage = HTImage(NoeBitStream(data))
    if htImage.parseHeader() != 0:
        return 0
  
    texList.append(NoeTexture("hardtrucktex", htImage.imageWidth, \
        htImage.imageHeight, htImage.getData(), noesis.NOESISTEX_RGBA32))   
    return 1
 
 
class MSKHeader: 
    def __init__(self): 
        self.magic = "MASK"
        self.imageWidth = 0
        self.imageHeight = 0  
        
    def toBytes(self):
        result = bytearray()
        result += self.magic.encode("ascii")       
        result += self.imageWidth.to_bytes(2, byteorder='little')
        result += self.imageHeight.to_bytes(2, byteorder='little')
        
        return result    
    
    
class TGAHeader:
    def __init__(self):
        self.idLength = 12
        self.colorMapType = 0
        self.imageType = 2
        self.firstEntryIndex = 0
        self.colorMapLength = 0
        self.colorMapEntrySize = 16
        self.xOrigin = 0
        self.yOrigin = 0
        self.imageWidth = 0
        self.imageHeight = 0
        self.pixelDepht = 16
        self.imageDescriptor = 32

    def toBytes(self):
        result = bytearray()
        result += self.idLength.to_bytes(1, byteorder='little')
        result += self.colorMapType.to_bytes(1, byteorder='little')
        result += self.imageType.to_bytes(1, byteorder='little')
        result += self.firstEntryIndex.to_bytes(2, byteorder='little')
        result += self.colorMapLength.to_bytes(2, byteorder='little')
        result += self.colorMapEntrySize.to_bytes(1, byteorder='little')
        result += self.xOrigin.to_bytes(2, byteorder='little')
        result += self.yOrigin.to_bytes(2, byteorder='little')
        result += self.imageWidth.to_bytes(2, byteorder='little')
        result += self.imageHeight.to_bytes(2, byteorder='little')
        result += self.pixelDepht.to_bytes(1, byteorder='little')
        result += self.imageDescriptor.to_bytes(1, byteorder='little')

        return result  

        
class exportDialogWindow:
    def __init__(self):
        self.options = {"Game":"ht2", "Format":"b5g5r5a1", \
            "GenerateMipMaps":"False"}
        self.isCanceled = True
        
    def exportOptionsButtonExport(self, noeWnd, controlId, wParam, lParam):
        index = self.gameListBox.getSelectionIndex()        
        if index == 0:
            self.options["Game"] = "ht1"
            
        index = self.formatComboBox.getSelectionIndex()        
        if index == 2:
            self.options["Format"] = "b5g5r5a1" 
        elif index == 0:
            self.options["Format"] = "b5g6r5" 
        else:
            self.options["Format"] = "b4g4r4a4"         
             
        if self.mipmapsCheckBox.isChecked():        
            self.options["GenerateMipMaps"] = "True" 
            
        self.isCanceled = False
        self.noeWnd.closeWindow()
        
        return True  
        
    def exportOptionsButtonCancel(self, noeWnd, controlId, wParam, lParam):
        self.noeWnd.closeWindow()
         
        return True    
    
    def show(self):   
        self.noeWnd = noewin.NoeUserWindow("Export options", "HTWindowClass", \
            300, 150) 
        noeWindowRect = noewin.getNoesisWindowRect()
        
        if noeWindowRect:
            windowMargin = 64
            self.noeWnd.x = noeWindowRect[0] + windowMargin
            self.noeWnd.y = noeWindowRect[1] + windowMargin   
            
        if self.noeWnd.createWindow():
            self.noeWnd.setFont("Arial", 12)    
            
            self.noeWnd.createStatic("Choose game:", 5, 5, 160, 20)
            # choose game list            
            index = self.noeWnd.createListBox(5, 25, 200, 47, None, 0)
            self.gameListBox = self.noeWnd.getControlByIndex(index)
            
            gameList = ("Hard Truck 1 (1.4)", "Hard Truck 2 (7.0 - 8.0)")
            
            for game in gameList:
                self.gameListBox.addString(game)               
            
            self.gameListBox.selectString(gameList[1])
                        
            self.noeWnd.createStatic("Choose format:", 5, 70, 110, 20)
            # choose format combobox           
            index = self.noeWnd.createComboBox(100, 67, 95, 20)
            self.formatComboBox = self.noeWnd.getControlByIndex(index)            
            
            formatList = ("BGR 565", "BGRA 4444", "BGRA 5551")            
            
            for format in formatList:
                self.formatComboBox.addString(format)             
            
            self.formatComboBox.selectString(formatList[2])
            
            index = self.noeWnd.createCheckBox("generate mip-maps", 5, 95, \
                 135, 20)
            self.mipmapsCheckBox = self.noeWnd.getControlByIndex(index) 
            #self.mipmapsCheckBox.setChecked(1)
            
            self.noeWnd.createButton("Export", 210, 25, 80, 30, \
                 self.exportOptionsButtonExport)
            self.noeWnd.createButton("Cancel", 210, 60, 80, 30, \
                 self.exportOptionsButtonCancel)
            
            self.noeWnd.doModal()   
   
   
def getOptions():
    # set export options
    options = {"Game":"", "Format":"b5g5r5a1", "GenerateMipMaps":"False"}
    
    if noesis.optWasInvoked("-htgame"): # set up with command line
        options["Game"] = noesis.optGetArg("-htgame")
        
    if noesis.optWasInvoked("-format"): # set up with command line
        options["Format"] = noesis.optGetArg("-format") 
        
    if noesis.optWasInvoked("-genmipmaps"): # set up with command line
        options["GenerateMipMaps"] = "True"        
        
    if options["Game"] == "":
        exportDialog = exportDialogWindow()
        exportDialog.show()
        if exportDialog.isCanceled:
            options["Game"] = "canceled"       
        else:
            options = exportDialog.options 
            
    print(options["Game"])
    print(options["Format"])
    
    return options
    

    # TODO: refactor this
def encodeImageRLE(imageData, imageWidth, imageBitDepth):   
    encodedData = bytearray()
    
    size = len(imageData)
   
    if imageBitDepth == 2:         
        imageData = unpack('H'*(len(imageData)//2), line)

    buffer = bytearray()
    rawCount = 0
    zeroCount = 0
    pos = 1
    
    for texel in imageData:                            
        if texel == 0: #       
            zeroCount += 1
            
            if zeroCount == 127:
                encodedData.append(zeroCount + 128)
                zeroCount = 0
                
            if rawCount > 0: # copy raw data
                encodedData.append(rawCount)
                encodedData += buffer
                buffer = bytearray()                  
                rawCount = 0
        else:            
            rawCount += 1
            buffer.append(texel) 
            
            if rawCount == 127:
                encodedData.append(rawCount)
                encodedData += buffer
                buffer = bytearray()                  
                rawCount = 0                
             
            if zeroCount > 0: #compressing zero pixels     
                encodedData.append(zeroCount + 128)
                zeroCount = 0
        
        if not(pos & imageWidth):
            if rawCount > 0: # copy raw data
                encodedData.append(rawCount)
                encodedData += buffer
                buffer = bytearray()                  
                rawCount = 0 
            else:
                encodedData.append(zeroCount + 128)
                zeroCount = 0             
        
        pos += 1
                  
    return encodedData    
    

def htMSKWriteRGBA(data, width, height, filewriter):
    options = getOptions()
    
    if options["Game"] != "canceled":    
        header = MSKHeader()
        header.imageWidth = width
        header.imageHeight = height 
        
        filewriter.writeBytes(header.toBytes())    
        
        # .msk files are packed with RLE compression 8 bit (Hard Truck 1) and
        # 16 bit (Hard Truck 2) images  
      
        if options["Game"] == "ht1":
            # get image palette and indexes
            pal = rapi.imageGetPalette(data, width, height, 256, 0, 0)
            palIndexes = rapi.imageApplyPalette(data, width, height, pal, 256)
        
            # encode indexes with RLE compression
            encodedData = encodeImageRLE(palIndexes, width, 1)
        
            # shrink palette to 768 
            palette = bytearray()            
            for i in range(0, 1024, 4):
                palette.append(pal[i + 2])
                palette.append(pal[i + 1])
                palette.append(pal[i])        
        
            filewriter.writeBytes(palette)
            filewriter.writeBytes(encodedData)
        else:  
            # hard truck 2 .msk files store empty palette
            emptyPalette = bytearray(768) 
            filewriter.writeBytes(emptyPalette)
        
            # encode 16 bit image data with RLE compression
            filewriter.writeBytes(encodeImageRLE(data, width, 2))
        
            pfrm = PFRM()
            filewriter.writeBytes(pfrm.toBytes()) # write bit masks 
        
            endr = ENDR()
            filewriter.writeBytes(endr.toBytes()) 
            
    return  1 
 
 
class ENDR:
    def __init__(self): 
        self.id = "ENDR"
        self.size = 0
        
    def toBytes(self):  
        result = bytearray()
        result += self.id.encode("ascii")
        result += self.size.to_bytes(4, byteorder='little')
        
        return result
        
        
class LOFF:
    def __init__(self): 
        self.id = "LOFF"
        self.size = 4
        self.offset = 0   
        
    def toBytes(self):     
        result = bytearray()
        result += self.id.encode("ascii")
        result += self.size.to_bytes(4, byteorder='little')
        result += self.offset.to_bytes(4, byteorder='little')
        
        return result
        
        
class PFRM:
    def __init__(self):     
        self.id = "PFRM"
        self.size = 28
        # bgra5551 by default
        self.redMask = 31744
        self.greenMask = 992
        self.blueMask = 31        
        self.alphaMask = 0
        self.emptyBytes = bytearray(12)
        
    def toBytes(self): 
        result = bytearray()
        result += self.id.encode("ascii")
        result += self.size.to_bytes(4, byteorder='little')
        result += self.redMask.to_bytes(4, byteorder='little')
        result += self.greenMask.to_bytes(4, byteorder='little')
        result += self.blueMask.to_bytes(4, byteorder='little')
        result += self.alphaMask.to_bytes(4, byteorder='little')        
        result += self.emptyBytes
        
        return result

class LVMP:
    def __init__(self):     
        self.id = "LVMP"
        self.size = 0
        self.count = 0
        self.mipWidth = 0
        self.mipHeight = 0
        self.bitDepth = 2
        
    def toBytes(self): 
        result = bytearray()
        result += self.id.encode("ascii")
        result += self.size.to_bytes(4, byteorder='little')
        result += self.count.to_bytes(4, byteorder='little')
        result += self.mipWidth.to_bytes(4, byteorder='little')
        result += self.mipHeight.to_bytes(4, byteorder='little')
        result += self.bitDepth.to_bytes(4, byteorder='little')
        
        return result        

    # TODO: refactor this      
def htTXRWriteRGBA(data, width, height, filewriter):
    options = getOptions()

    if options["Game"] != "canceled":   
        header = TGAHeader()
        header.imageWidth = width
        header.imageHeight = height  
        
        if options["Game"] == "ht1": 
            # Hard Truck 1 textures are 8 bit images with 256 palette

            if options["GenerateMipMaps"] == "True" and width > 2:
                header.idLength = 12
            else:            
                header.idLength = 0
            header.colorMapType = 1
            header.imageType = 1
            header.colorMapLength = 256
            header.colorMapEntrySize = 24
            header.pixelDepht = 8 
        
            filewriter.writeBytes(header.toBytes())
        
            if options["GenerateMipMaps"] == "True" and width > 2:
                loff = LOFF()
                loff.offset = width * height + 30 + 768
                filewriter.writeBytes(loff.toBytes())        
        
            pal = rapi.imageGetPalette(data, width, height, 256, 0, 0)

            # shrink palette to 768 
            palette = bytearray()            
            for i in range(0, 1024, 4):
                palette.append(pal[i + 2])
                palette.append(pal[i + 1])
                palette.append(pal[i])
            
            palIndexes = rapi.imageApplyPalette(data, width, height, pal, 256)
            
            filewriter.writeBytes(palette)
            filewriter.writeBytes(palIndexes)
            
            if options["GenerateMipMaps"] == "True" and width > 2:
                mapCountList = {2048:10, 1024:10, 512:9, 256:8, 128:7, 64:6, \
                    32:5, 16:4, 8:3, 4:2, 2:1}
                             
                lvmp = LVMP()            
                lvmp.count = mapCountList.get(width)
                # TODO: check for image size
                lvmp.mipWidth = int(width / 2)
                lvmp.mipHeight = int(height / 2)
                lvmp.bitDepth = 1    
                       
                mipMapsData = bytes()
                for i in range(1, lvmp.count + 1):
                    mipMapWidth = max(width >> i, 1)
                    mipMapHeight = max(height >> i, 1)
                    mipMap = rapi.imageResample(data, width, height, \
                        mipMapWidth, mipMapHeight)
                    mipMapData = rapi.imageApplyPalette(mipMap, mipMapWidth, \
                        mipMapHeight, pal, 256)    
                    mipMapsData += mipMapData
                 
                empty = bytearray(2) # ?!
                mipMapsData += empty              
                
                lvmp.size = len(mipMapsData) + 13
                filewriter.writeBytes(lvmp.toBytes())
                filewriter.writeBytes(mipMapsData)                 
        else: 
            # Hard Truck 2 textures are 16 bit images + empty 256 palette         
            filewriter.writeBytes(header.toBytes())

            loff = LOFF()
            loff.offset = width * height * 2 + 30
            filewriter.writeBytes(loff.toBytes())
        
            imageData = rapi.imageEncodeRaw(data, width, height, options["Format"]) 
            filewriter.writeBytes(imageData)
            
            if options["GenerateMipMaps"] == "True" and width > 2:
                mapCountList = {2048:10, 1024:10, 512:9, 256:8, 128:7, 64:6, \
                    32:5, 16:4, 8:3, 4:2, 2:1}
                             
                lvmp = LVMP()            
                lvmp.count = mapCountList.get(width)
                # TODO: check for image size
                lvmp.mipWidth = int(width / 2)
                lvmp.mipHeight = int(height / 2)
                lvmp.bitDepth = 2    
                                 
                mipMapsData = bytes()
                for i in range(1, lvmp.count + 1):
                    mipMapWidth = max(width >> i, 1)
                    mipMapHeight = max(height >> i, 1)
                    mipMap = rapi.imageResample(data, width, height, \
                        mipMapWidth, mipMapHeight)
                    mipMapData = rapi.imageEncodeRaw(mipMap, mipMapWidth, \
                        mipMapHeight, options["Format"])    
                    mipMapsData += mipMapData
                 
                empty = bytearray(2) # ?!
                mipMapsData += empty
                 
                lvmp.size = len(mipMapsData) + 14  
                filewriter.writeBytes(lvmp.toBytes()) 
                filewriter.writeBytes(mipMapsData)    
                     
            pfrm = PFRM()
            
            if options["Format"] == "b5g6r5":
                pfrm.redMask = 63488
                pfrm.greenMask = 2016
                pfrm.blueMask = 31        
                pfrm.alphaMask = 0  
                
            if options["Format"] == "b4g4r4a4":
                pfrm.redMask = 3840
                pfrm.greenMask = 240
                pfrm.blueMask = 15        
                pfrm.alphaMask = 61440   
                
            filewriter.writeBytes(pfrm.toBytes()) 
       
            endr = ENDR()
            filewriter.writeBytes(endr.toBytes())   
    
    return  1   
