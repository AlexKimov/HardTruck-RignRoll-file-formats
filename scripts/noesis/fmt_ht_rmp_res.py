from inc_noesis import *
import os

def registerNoesisTypes():
    handle = noesis.register("Hard Truck 1/2 Resource archive", ".res;.rmp")
    noesis.setHandlerExtractArc(handle, resExtractRes)
     
    return 1
    
 
def resExtractRes(fileName, fileLen, justChecking):
    with open(fileName, "rb") as f:
        if justChecking: #it's valid
            return 1        
        fileSections = ("PALETTEFILES", "SOUNDFILES", "TEXTUREFILES", \
                "BACKFILES", "MASKFILES") 
                
        propertySections = ("COLORS", "MATERIALS", "SOUNDS")                
                            
        filereader = NoeBitStream(f.read());
         
        proStrings = []
         
        while filereader.tell() < filereader.getSize():
            str = filereader.readString()
            proStrings.append(str + '\n')
            name, count = str.split(" ")            
            if name in fileSections:
                for x in range(int(count)):
                    fname = filereader.readString()
                    proStrings.append(fname + '\n')
                    
                    size = filereader.readUInt()               
                    fdata = filereader.readBytes(size)
                    
                    print("Extracting " + fname.split(" ")[0])
                    
                    rapi.exportArchiveFile(fname.split(" ")[0], fdata)
            elif name in propertySections: 
                for x in range(int(count)):                  
                    proStrings.append(filereader.readString() + '\n')
            else:
                noesis.doException("Error: Wrong format.")
                    
    # write .pro file
    proFilename = rapi.getOutputName() + os.path.basename(fileName) + '.pro'
    with open(proFilename, "w") as text:
        text.writelines(proStrings)
               
    return 1