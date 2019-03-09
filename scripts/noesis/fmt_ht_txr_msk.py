from inc_noesis import *
import os
from timeit import default_timer as timer
from struct import unpack


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 1/2 Textures", ".txr;.msk")
    noesis.setHandlerTypeCheck(handle, htCheckType)
    noesis.setHandlerLoadRGBA(handle, htLoadRGBA)
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
        filereader.seek(8, NOESEEK_REL)
        self.bitsRed = filereader.readUInt()
        self.bitsGreen = filereader.readUInt()
        self.bitsBlue = filereader.readUInt()
        self.bitsAlpha = filereader.readUInt()  
    
    def readTXRHeader(self, filereader):
        # actually TGA header
        self.IDLength = filereader.readByte()
        
        filereader.seek(12, NOESEEK_ABS)
        
        self.imageWidth = filereader.readShort()
        self.imageHeight = filereader.readShort()
        
        self.bitDepth = filereader.readByte() # 8 - Hard Truck 1, 16 - HT 2
        
        filereader.seek(1 + self.IDLength, NOESEEK_REL)
        
        self.imageSize = self.imageWidth*self.imageHeight

        return 0        
     
    def readMSKHeader(self, filereader):
        self.magic = filereader.readUInt() 
        
        self.imageWidth = filereader.readShort()
        self.imageHeight = filereader.readShort() 
        
        self.imageSize = self.imageWidth*self.imageHeight
        return 0 
        
    def palettedToRGBA32(self, palBuffer, indBuffer):       
        imageData = bytearray()
        
        palBuffer = memoryview(palBuffer)
        alpha = memoryview(bytes([255]))
        
        #start = timer()  
        
        for index in indBuffer:
            imageData += palBuffer[index*3 + 2]            
            imageData += palBuffer[index*3 + 1]
            imageData += palBuffer[index*3]            
            imageData += alpha[0]
            
        #end = timer()       
        #print(end - start)   
        
        return imageData
                
    def getPalettedImageFromFile(self, filereader):
                  
        palBuffer = filereader.readBytes(filereader.tell() + 768)
        indBuffer = filereader.greadBytes(self.imageSize)    
                
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
                
        #noesis.logPopup()
        #print(filereader.tell()) 
        
        return unpackedImageData
    
    def unpackRGBAImage(self, filereader):        
        # goto PFRM section to read bit masks
        self.bitMaskPos = filereader.getSize() - 44 
        filereader.seek(self.bitMaskPos, NOESEEK_ABS)
        self.readBitMask(filereader)
        
        # return to RLE packed image data
        filereader.seek(768 + 8, NOESEEK_ABS) # 8 - header size
        
        imageBuffer = self.unpackRLEImageData(filereader)       

        return self.getRGBAImage(imageBuffer) 
        
    def unpackPalettedImage(self, filereader):
        # get palette
        palBuffer = filereader.readBytes(768)
        # get packed indexes
        imageDataBuffer = filereader.getBuffer()[filereader.tell():]
      
        self.bitMaskPos = filereader.getSize()
        
        # unpack (RLE compression) palette indexes        
        indBuffer = self.unpackRLEImageData(filereader, imageDataBuffer)
        
        return self.palettedToRGBA32(palBuffer, indBuffer)
    
    def getRGBAImage(self, imageBuffer):
    
        buffer = unpack('H'*(len(imageBuffer)//2), imageBuffer)
    
        # bit unpack tables
        #table2 = [0, 255] 
        table16 = bytes([0, 17, 34, 51, 68, 86, 102, 119, 136, 153, 170, 181, \
            204, 221, 238, 255])
        table32 = bytes([0, 8, 16, 25, 33, 41, 49, 58, 66, 74, 82, 90, 99, \
            107, 115, 123, 132, 140, 148, 156, 165, 173, 181, 189, 197, 206, \
            214, 222, 230, 239, 247, 255])
        table64 = bytes([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 49, 53, \
            57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, \
            117, 121, 125, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, \
            170, 174, 178, 182, 186, 190, 194, 198, 202, 206, 210, 215, 219, \
            223, 227, 231, 235, 239, 243, 247, 251, 255])   
 
        # speed up a little bit
        table16 = memoryview(table16)
        table32 = memoryview(table32)
        table64 = memoryview(table64)
        
        imageData = bytearray()  
        
        #unpack RGBA 16 bit to RGBA 32 bit       
        for pixel in buffer:        
           if self.bitsRed == 63488: # RGB 565             
               imageData += table32[(pixel >> 11) & 31] 
               imageData += table64[(pixel >> 5) & 63] 
               imageData += table32[pixel & 31] 
               imageData += table32[31] # 255 - alpha               
           elif self.bitsRed == 31744: # RGB 5551          
               imageData += table32[(pixel >> 10) & 31] 
               imageData += table32[(pixel >> 5) & 31]               
               imageData += table32[pixel & 31]  
               imageData += table32[31]
           else: # RGBA 4444            
               imageData += table16[(pixel >> 8) & 15]  
               imageData += table16[(pixel >> 4) & 15]                
               imageData += table16[pixel & 15] 
               imageData += table16[(pixel >> 12) & 15]                 
            
        return imageData 
        
    def getRGBAImageFromFile(self, filereader):
        # bit unpack tables
        #table2 = [0, 255] 
        table16 = bytes([0, 17, 34, 51, 68, 86, 102, 119, 136, 153, 170, 181, \
            204, 221, 238, 255])
        table32 = bytes([0, 8, 16, 25, 33, 41, 49, 58, 66, 74, 82, 90, 99, \
            107, 115, 123, 132, 140, 148, 156, 165, 173, 181, 189, 197, 206, \
            214, 222, 230, 239, 247, 255])
        table64 = bytes([0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 49, 53, \
            57, 61, 65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, \
            117, 121, 125, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, \
            170, 174, 178, 182, 186, 190, 194, 198, 202, 206, 210, 215, 219, \
            223, 227, 231, 235, 239, 243, 247, 251, 255])   
      
        # get image from file
        imageBuffer = filereader.readBytes(self.imageSize*2)     
        
        self.readBitMask(filereader)  
        
        return self.getRGBAImage(imageBuffer)                
            
    def readTXRdata(self, filereader):
        if self.bitDepth == 8:
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
    
    def parseHeader(self):
        self.extension = os.path.splitext(rapi.getInputName())[1]
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

