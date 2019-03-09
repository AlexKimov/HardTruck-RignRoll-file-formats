from inc_noesis import *
import os

def registerNoesisTypes():
    handle = noesis.register("Hard Truck 1/2 Resource archive", ".res;.rmp")
    noesis.setHandlerExtractArc(handle, resExtractRes)
    
    #handle = noesis.register("Hard Truck 1/2 Textures", ".msk;.res")
    #noesis.setHandlerTypeCheck(handle, artCheckType)
    #noesis.setHandlerLoadRGBA(handle, artLoadRGBA)    
    return 1
    
 
def resExtractRes(fileName, fileLen, justChecking):
    with open(fileName, "rb") as f:
        if justChecking: #it's valid
            return 1        
        fileSections = ("PALETTEFILES", "SOUNDFILES", "TEXTUREFILES", \
                "BACKFILES", "MASKFILES") 
                
        filereader = NoeBitStream(f.read());
         
        proStrings = []
         
        while filereader.tell() < filereader.getSize():
            name, count = filereader.readString().split(" ")
            proStrings.append(name + '\n')
            if name in fileSections:
                for x in range(int(count)):
                    fname = filereader.readString()
                    size = filereader.readUInt()               
                    fdata = filereader.readBytes(size)
                    print("Extracting " + fname)
                    rapi.exportArchiveFile(fname, fdata)
                    proStrings.append(fname + '\n')
            else: 
                for x in range(int(count)):                  
                    proStrings.append(filereader.readString() + '\n')
                    
    # write .pro file
    proFilename = rapi.getOutputName() + os.path.basename(fileName) + '.pro'
    with open(proFilename, "w") as text:
        text.writelines(proStrings)
               
    return 1