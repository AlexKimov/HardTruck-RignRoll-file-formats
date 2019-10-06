from inc_noesis import *
import os
import noewin


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 1/2 Resource archive", ".res;.rmp;.pro")
    noesis.setHandlerExtractArc(handle, resExtractRes)
    
    toolHandle = noesis.registerTool("Pack HT Resource", \
        htResourcePackerToolMethod, "Pack files to game archive.")
    noesis.setToolFlags(toolHandle, noesis.NTOOLFLAG_CONTEXTITEM)
    noesis.setToolVisibleCallback(toolHandle, htArchivePackerVisible) 
    
    return 1

    
class proFile:
    def __init__(self, filename):
        self.filename = filename  
        self.sections = {}
    
    def read(self):
        with open(self.filename, "r") as textFile:
            try:
                for line in textFile:
                    name, count = line.split(" ") 

                    sectionItems = []
                    for i in range(int(count)):
                        line = textFile.readline()
                        sectionItems.append(line[0:-1])
                            
                    self.sections.update({name:sectionItems})
                                       
            except:
                noesis.messagePrompt( \
                    "Can't read {} file.".format(self.filename))                
                return 0

        #noesis.logPopup()
        #for key, value in self.sections.items():
        #    print(key)                 
        return 1
       
       
class htArchivePacker:
    def __init__(self, filename):
        self.path = os.path.dirname(filename)
        
        self.proFile = proFile(filename)      
        self.proFile.read()
        
        self.filesSectionName = ("TEXTUREFILES", "PALETTEFILES", "SOUNDFILES", \
            "BACKFILES", "MASKFILES")      
      
    def outputLog(self, logStrings):
        with open(self.proFile.filename + ".log", "w") as text:         
            text.writelines(logStrings)     
    
    def checkFiles(self):
        log = []
        #noesis.logPopup()
        for section, items in self.proFile.sections.items():        
            if section in self.filesSectionName:
                log.append("Checking '{}' files...\n".format(section))
                warningCount = 0             
                for name in items:
                    name = name.split(" ")[0]                
                    if not os.path.isfile(os.path.join(self.path, name)):                
                        log.append( \
                            "Warning: file {} doesn't exist.\n".format(name))
                        warningCount += 1
                if warningCount == 0:
                    log.append("Result: All OK. \n") 
                else:                    
                    log.append(\
                        "Result: {} problem files.\n".format(warningCount))  
                    
        self.outputLog(log)
        return log
            
    def packArchive(self, extension = ""):
        log = []
        
        if extension != "":
            archiveName = self.proFile.filename.split(".")[0] + extension
        else:
            filename, archiveExtension, pro = self.proFile.filename.split(".")
            archiveName = filename + '.' + archiveExtension  
         
        warningCount = 0  
         
        with open(archiveName, "wb") as archiveFile:
            #noesis.logPopup()           
            for section, items in self.proFile.sections.items():
                str = "{} {}\0".format(section, len(items))            
                archiveFile.write(str.encode("ascii"))    
                
                if section in self.filesSectionName:
                    for name in items:
                        try:                         
                            with open(os.path.join(\
                                self.path, name.split(" ")[0]), "rb") as htFile:
                                file = htFile.read()
                            # write filename 
                            archiveFile.write((name + '\0').encode("ascii"))
                        
                            # write file size 
                            fileSize = len(file).to_bytes(4, byteorder='little')                         
                            archiveFile.write(fileSize)
                        
                            # write file itself
                            archiveFile.write(file)                               
                        except:
                            log.append( \
                              "File {} failed to add.\n".format( \
                              os.path.join(self.path, name)))
                            warningCount += 1
                else:               
                    for item in items: 
                        try:                     
                            archiveFile.write((item + "\0").encode("ascii"))
                        except:                        
                            log.append("Item {} failed to add.\n".format(item))
                            warningCount += 1
                            
        if warningCount == 0:
            log.append("Archive {} packed successfully.\n".format(archiveName))
                
        self.outputLog(log)
        return log
        
        
class archivePackerDialogWindow():
    def __init__(self, filename):
        self.isCanceled = True
        self.filename = filename
     
    def archivePackerButtonCheck(self, noeWnd, controlId, wParam, lParam):              
        output = ""
        for line in self.packer.checkFiles():
            output += line
        self.outputEdit.setText("")    
        self.outputEdit.setText(output)
        
        return True  
    
    def archivePackerButtonPack(self, noeWnd, controlId, wParam, lParam):
        output = ""
        for line in self.packer.packArchive():
            output += line
        self.outputEdit.setText("")    
        self.outputEdit.setText(output)     
        
        self.isCanceled = False
        
        return True  
        
    def archivePackerButtonCancel(self, noeWnd, controlId, wParam, lParam):
        self.noeWnd.closeWindow()
         
        return True    
    
    def create(self):   
        self.noeWnd = noewin.NoeUserWindow( \
            "Hard Truck archive packer (.res, .rmp)", "HTPackerWindowClass", \
            420, 255) 
        noeWindowRect = noewin.getNoesisWindowRect()
        
        if noeWindowRect:
            windowMargin = 100
            self.noeWnd.x = noeWindowRect[0] + windowMargin
            self.noeWnd.y = noeWindowRect[1] + windowMargin   
            
        if self.noeWnd.createWindow():
            self.noeWnd.setFont("Arial", 12)    
            
            self.noeWnd.createStatic("File path:", 5, 5, 50, 20)
            #            
            index = self.noeWnd.createEditBox(60, 5, 350, 20, "", None, \
                False, True)
            self.pathEdit = self.noeWnd.getControlByIndex(index)
            self.pathEdit.setText(self.filename)
            
            self.noeWnd.createStatic("Exten.:", 5, 32, 110, 20)
            #           
            index = self.noeWnd.createComboBox(60, 32, 130, 20)
            self.extComboBox = self.noeWnd.getControlByIndex(index)            
            
            extList = ("", "Hard Truck 1 (.rmp)", "Hard Truck 2 (.res)")            
            
            for extension in extList:
                self.extComboBox.addString(extension)              
            
            self.extComboBox.selectString(extList[0])
            
            self.noeWnd.createStatic("Output:", 5, 65, 60, 20)
            #            
            index = self.noeWnd.createEditBox(60, 65, 350, 120, "", None, \
                True, True)
            self.outputEdit = self.noeWnd.getControlByIndex(index)            
            
            self.noeWnd.createButton("Check files", 60, 195, 80, 30, \
                 self.archivePackerButtonCheck)            
            self.noeWnd.createButton("Pack archive", 145, 195, 80, 30, \
                 self.archivePackerButtonPack)
            self.noeWnd.createButton("Cancel", 330, 195, 80, 30, \
                 self.archivePackerButtonCancel)
            
            self.packer = htArchivePacker(self.filename)
            
            self.noeWnd.doModal()   
            
    
#see if the pvr reorder context tool should be visible
def htArchivePackerVisible(toolIndex, selectedFile):
    if selectedFile is None or \
            os.path.splitext(selectedFile)[1].lower() != ".pro":            
        return 0
        
    return 1
 
 
def htResourcePackerToolMethod(toolIndex):
    srcPath = noesis.getSelectedFile()
    
    if srcPath is None or os.path.exists(srcPath) is not True:
        noesis.messagePrompt( \
            "Selected file isn't readable through the standard filesystem.")
            
        return 0
        
    archivePackerDialogWindow(srcPath).create()       
        
    return 1 
 
 
def resExtractRes(fileName, fileLen, justChecking):
    if os.path.splitext(fileName)[1].lower() == ".pro":
        archivePackerDialogWindow(fileName).create()    
    else:
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