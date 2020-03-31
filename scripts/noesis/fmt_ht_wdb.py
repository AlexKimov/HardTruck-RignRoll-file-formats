#
#
#


from inc_noesis import *
import os
import noewin
import noewinext
from collections import OrderedDict 


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 3 Resource", ".wdb")
    noesis.setHandlerExtractArc(handle, wdbExtractResources)
    
    return 1
  
  
class DDSPixelFormat:
    def __init__(self, format=0): 
        self.dwSize = 32
        if format == 26: #rgba4444
          self.dwFlags = 64
          self.dwFourCC = 0
          self.dwRGBBitCount = 16
          self.dwRBitMask = 3840
          self.dwGBitMask = 240
          self.dwBBitMask = 15
          self.dwABitMask = 61440       
        elif format == 21: #A8R8G8B8
          self.dwFlags = 65
          self.dwFourCC = 0
          self.dwRGBBitCount = 32
          self.dwRBitMask = 16711680
          self.dwGBitMask = 65280
          self.dwBBitMask = 255
          self.dwABitMask = 4278190080    
        elif format == 22: #X8R8G8B8
          self.dwFlags = 65
          self.dwFourCC = 0
          self.dwRGBBitCount = 32
          self.dwRBitMask = 16711680
          self.dwGBitMask = 65280
          self.dwBBitMask = 255
          self.dwABitMask = 0            
        else: #DXT compression
          self.dwFlags = 4
          self.dwFourCC = format
          self.dwRGBBitCount = 0
          self.dwRBitMask = 0
          self.dwGBitMask = 0
          self.dwBBitMask = 0
          self.dwABitMask = 0  
        
    def toBytes(self): 
        result = bytearray()
        result += self.dwSize.to_bytes(4, byteorder='little')
        result += self.dwFlags.to_bytes(4, byteorder='little')
        result += self.dwFourCC.to_bytes(4, byteorder='little')
        result += self.dwRGBBitCount.to_bytes(4, byteorder='little')
        result += self.dwRBitMask.to_bytes(4, byteorder='little') 
        result += self.dwGBitMask.to_bytes(4, byteorder='little')
        result += self.dwBBitMask.to_bytes(4, byteorder='little')
        result += self.dwABitMask.to_bytes(4, byteorder='little')
        
        return result
        
    
class DDSHeader:
    def __init__(self, width=0, height=0, format=0, size=0, mmcount=1):
        self.magic = 542327876
        self.dwSize = 124
        self.dwFlags = 4111 #528391
        self.dwHeight = width
        self.dwWidth = height
        self.dwPitchOrLinearSize = size
        self.dwDepth = 0
        self.dwMipMapCount = mmcount
        self.dwReserved1 = bytearray(44)
        self.ddspf = DDSPixelFormat(format)
        self.dwCaps = 4096
        self.dwCaps2 = 0
        self.dwCaps3 = 0
        self.dwCaps4 = 0
        self.dwReserved2 = 0    
        
    def toBytes(self): 
        result = bytearray()
        result += self.magic.to_bytes(4, byteorder='little')
        result += self.dwSize.to_bytes(4, byteorder='little')
        result += self.dwFlags.to_bytes(4, byteorder='little')
        result += self.dwHeight.to_bytes(4, byteorder='little')
        result += self.dwWidth.to_bytes(4, byteorder='little')
        result += self.dwPitchOrLinearSize.to_bytes(4, byteorder='little')  
        
        result += self.dwDepth.to_bytes(4, byteorder='little')
        result += self.dwMipMapCount.to_bytes(4, byteorder='little')
        result += self.dwReserved1
        result += self.ddspf.toBytes()
        result += self.dwCaps.to_bytes(4, byteorder='little')  
        result += self.dwCaps2.to_bytes(4, byteorder='little')  
        result += self.dwCaps3.to_bytes(4, byteorder='little')  
        result += self.dwCaps4.to_bytes(4, byteorder='little')  
        result += self.dwReserved2.to_bytes(4, byteorder='little')
        
        return result                


class WDBMaterial:
    def __init__(self):
        self.nText = 0
        self.ParamName = ""
        self.ParamValue = 0 

    def read(self, reader):
        reader.seek(4, NOESEEK_REL)
        reader.readString()
        reader.seek(4, NOESEEK_REL)    
        
        
class WDBTextureContainer:
    def __init__(self, name):
        self.name = name
        self.textures = []


class WDBTexture:
    def __init__(self):
        self.format = 0
        self.width = 0
        self.height = 0
        self.dataSize = 0
        self.data = None
        
    def read(self, reader):
        self.format = reader.readUInt()
        self.height = reader.readUShort()
        self.width = reader.readUShort()
        self.dataSize = reader.readUInt()
        self.data = reader.readBytes(self.dataSize)


class WDBObject:
    def __init__(self, name, type):
        self.name = name
        self.type = type
 
 
class WDFFile:
    def __init__(self, reader):
        self.reader = reader
        self.materials = []
        self.textures = []
        self.prevObj = None

    def readHeader(self, reader):        
        reader.seek(108 + 8, NOESEEK_REL)  
        
    def readTable(self, reader, parentObj=None): 
        reader.seek(8, NOESEEK_REL)
        reader.readString() 
        
        count = reader.readUInt()
        for i in range(count): 
            reader.seek(12, NOESEEK_REL)    

        reader.seek(4, NOESEEK_REL)
        for i in range(count): 
            reader.readString()               
        
    def readChunk(self, reader):
        type = reader.readUInt() 
        size = reader.readUInt()
        name = reader.readString()

        if type == 201: #??        
            reader.readUInt()
            reader.seek(64, NOESEEK_REL)           
        elif type == 404:     
            count = reader.readUInt()
            for number in range(count): 
                self.readChunk(reader)                
        elif type == 307:     
            count = reader.readUInt()
            if name == "":
                name = self.prevObj.name            
            textureContainer = WDBTextureContainer(name)
            self.textures.append(textureContainer)
            self.prevObj = WDBObject(name, type) 
            for number in range(count): 
                self.readChunk(reader)                                
        elif type == 306:         
            texture = WDBTexture()
            texture.read(reader)         
            
            if name != "":
                self.textures.append(WDBTextureContainer(name))            
            else:
                if self.prevObj.type == 320:
                    self.textures.append(WDBTextureContainer(self.prevObj.name))  
            self.textures[len(self.textures) - 1].textures.append(texture)                           
        elif type == 320:   
            reader.readString()           
            count = reader.readUInt()
            self.prevObj = WDBObject(name, type) 
            for matNumber in range(count):
                self.readChunk(reader) 
            
            propCount = reader.readUInt()            
            for propNumber in range(propCount):
                material = WDBMaterial()
                material.read(reader) 
                
                self.materials.append(material)
        else:
            reader.seek(size - 8 - len(name) - 1, NOESEEK_REL) 
             
    def readData(self, reader):    
        self.readChunk(reader)    
         
    def read(self): 
        self.readHeader(self.reader)
        self.readTable(self.reader)       
        self.readData(self.reader)        
    
    
def wdbExtractResources(fileName, fileLen, justChecking):    
    with open(fileName, "rb") as f:
        if justChecking: #it's valid
            return 1   
        
        filereader = NoeBitStream(f.read())    
    
        wdb = WDFFile(filereader)
        wdb.read()
          
        for container in wdb.textures:            
            name = '{}.dds'.format(container.name)
            texture = container.textures[0]
            header = DDSHeader(texture.width, texture.height, texture.format, 
                texture.dataSize, len(container.textures))                     
            data = bytes() 
            for texture in container.textures:            
                data += texture.data
            
            rapi.exportArchiveFile(name, header.toBytes() + data)
       
    return 1