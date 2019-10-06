from inc_noesis import *
import time
import os 
import noewin


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 2 King of The Road heightmap", ".raw")
    noesis.setHandlerTypeCheck(handle, rawCheckType)
    noesis.setHandlerLoadModel(handle, rawLoadModel)
    # noesis.setHandlerWriteModel(handle, rawWriteModel)
    
    noesis.addOption(handle, "-heightcoeff", "height coefficient (0..1)", noesis.OPTFLAG_WANTARG)
    noesis.addOption(handle, "-sealevel", "sea level (0..255)", noesis.OPTFLAG_WANTARG)

    return 1
 

DEFAULT_HEIGHT_COEFF = 0.22
DEFAULT_SAND_LEVEL = 90
DEFAULT_HEIGHTMAP_SIZE = 257
DEFAULT_UTILE = 1  
DEFAULT_VTILE = 1 
DEFAULT_SCALE = 1


class RAWFile:
    def __init__(self, reader, heightmapSize=DEFAULT_HEIGHTMAP_SIZE):
        self.reader = reader
        self.heightsData = []
        self.vertInRowCount = heightmapSize

    def readHeightMap(self, filereader):
        # raw file stores the heightmap 256x256 in size
        for row in range(self.vertInRowCount):
            line = bytearray() 
            for col in range(self.vertInRowCount):
                line.append(filereader.readUByte())          
                filereader.seek(1, NOESEEK_REL)  # skip one bit
            self.heightsData.append(line)
            
        return 1
    
    def read(self):
        self.readHeightMap(self.reader)
        
        return 1  

        
class faceVertex:
    def __init__(self):
        self.pos = ()
        self.uv = ()
   
   
class heightmapSurface:
    def __init__(self):
        self.faces = []
        self.materialName = ""
        
    def addFace(self, face):
        self.faces.append(face)
        
        
class heightmapMesh:
    def __init__(self, heightmap, heightCoeff=DEFAULT_HEIGHT_COEFF, seaLevel=DEFAULT_SAND_LEVEL,
                 utile=DEFAULT_UTILE, vtile=DEFAULT_VTILE):
        self.utileValue = utile 
        self.vtileValue = vtile
        
        self.heights = heightmap
        self.heightCoeff = heightCoeff
        self.seaLevel = seaLevel * heightCoeff  
        
        #self.materialNames = ["ter000.txr", "ter100.txr"]
        self.textures = []
        self.materials = []

        self.surfaces = []       
        sands = heightmapSurface()
        sands.materialName = "ter000.txr" 
        self.surfaces.append(sands) 
        
        rocks = heightmapSurface()
        rocks.materialName = "ter100.txr"        
        self.surfaces.append(rocks)  
        
    def addFace(self, vert1, vert2, vert3):
        meanHeight = (vert1.pos[2] + vert2.pos[2] + vert3.pos[2]) / 3
        
        if meanHeight <= self.seaLevel:       
            self.surfaces[0].addFace((vert1, vert2, vert3)) 
        else:    
            self.surfaces[1].addFace((vert1, vert2, vert3))          
 
    def loadTextures(self): 
        for surface in self.surfaces:
            try:    
                name = surface.materialName            
                texture = rapi.loadExternalTex(name)
                if texture != None:
                    self.textures.append(texture)            
                    material = NoeMaterial(name.split(".")[0], name)
                    material.setFlags(0, 1)
                    self.materials.append(material)
            except: 
                print("Can't load texture ", name) 
                
        return 1
 
    def buildFaces(self):    
        heightmapSize = DEFAULT_HEIGHTMAP_SIZE
        
        utile = self.utileValue/(heightmapSize - 1)
        vtile = self.vtileValue/(heightmapSize - 1) 
        
        # building faces (triangles)
        for row in range(0, heightmapSize - 2):
            for col in range(0, heightmapSize - 1):
                # first triangle 
                vertex1 = faceVertex()
                vertex1.pos = ((col + 1), (row), self.heights[row][col + 1] * \
                    self.heightCoeff)
                vertex1.uv = (utile*col, vtile*row) 
                 
                vertex2 = faceVertex()  
                vertex2.pos = (col, row, self.heights[row][col] * \
                    self.heightCoeff)
                vertex2.uv = (utile*col, vtile*row)

                vertex3 = faceVertex()                     
                vertex3.pos = (col, row + 1, self.heights[row + 1][col] * \
                    self.heightCoeff)
                vertex3.uv = (utile*col, vtile*row)
                          
                self.addFace(vertex1, vertex2, vertex3)  
                
                # second triangle
                vertex1 = faceVertex()                
                vertex1.pos = (col + 1, row + 1, self.heights[row + 1][col + 1] * \
                    self.heightCoeff)
                vertex1.uv = (utile*col, vtile*row)
                
                vertex2 = faceVertex()    
                vertex2.pos = (col + 1, row, self.heights[row][col + 1] * \
                    self.heightCoeff)
                vertex2.uv = (utile*col, vtile*row)
                
                vertex3 = faceVertex()    
                vertex3.pos = (col, row + 1, self.heights[row + 1][col] * \
                    self.heightCoeff)
                vertex3.uv = (utile*col, vtile*row)
                
                self.addFace(vertex1, vertex2, vertex3) 
       
    def create(self): 
        self.buildFaces()
        self.loadTextures()

    
def rawCheckType(data):

    return 1
   
 
def isNumber(number):
    try:
        float(number)
    except:
        return 0
        
    return 1    
   
    
class openOptionsDialogWindow:
    def __init__(self):
        self.options = {"HeightCoefficient": DEFAULT_HEIGHT_COEFF, "SandLevel": DEFAULT_SAND_LEVEL,
                        "UTile": DEFAULT_UTILE, "VTile": DEFAULT_VTILE, "Scale": DEFAULT_SCALE}
            
        self.isCanceled = True
        
    def openOptionsButtonImport(self, noeWnd, controlId, wParam, lParam):

        height = self.heightEdit.getText()
        if isNumber(height):
            self.options["HeightCoefficient"] = float(height)  
            
        level = self.levelEdit.getText()
        if isNumber(level):        
            self.options["SandLevel"] = float(level) 
            
        scale = self.scaleEdit.getText() 
        if isNumber(scale):        
            self.options["Scale"] = float(scale) 
   
        utile = self.utileEdit.getText() 
        if isNumber(utile):        
            self.options["UTile"] = float(utile) 

        vtile = self.vtileEdit.getText() 
        if isNumber(vtile):        
            self.options["VTile"] = float(vtile)
            
        self.isCanceled = False
        self.noeWnd.closeWindow()
       
        return True  
        
    def openOptionsButtonCancel(self, noeWnd, controlId, wParam, lParam):
        self.noeWnd.closeWindow()
         
        return True    
    
    def create(self):   
        self.noeWnd = noewin.NoeUserWindow("Import options", "HTRAWWindowClass", \
            286, 180) 
        noeWindowRect = noewin.getNoesisWindowRect()
        
        if noeWindowRect:
            windowMargin = 100
            self.noeWnd.x = noeWindowRect[0] + windowMargin
            self.noeWnd.y = noeWindowRect[1] + windowMargin   
            
        if self.noeWnd.createWindow():
            self.noeWnd.setFont("Arial", 12)    
            
            self.noeWnd.createStatic("Height coefficient:", 5, 7, 120, 20)
            #            
            index = self.noeWnd.createEditBox(110, 5, 70, 20, None, 0)
            self.heightEdit = self.noeWnd.getControlByIndex(index)
            self.heightEdit.setText(str(DEFAULT_HEIGHT_COEFF))
                           
            self.noeWnd.createStatic("Sand level:", 43, 32, 120, 20)
            #            
            index = self.noeWnd.createEditBox(110, 30, 70, 20, None, 0)
            self.levelEdit = self.noeWnd.getControlByIndex(index)
            self.levelEdit.setText(str(DEFAULT_SAND_LEVEL))
            
            self.noeWnd.createStatic("Scale:", 69, 57, 120, 20)
            #            
            index = self.noeWnd.createEditBox(110, 55, 70, 20, None, 0)
            self.scaleEdit = self.noeWnd.getControlByIndex(index)
            self.scaleEdit.setText(str(DEFAULT_SCALE))
            
            index = self.noeWnd.createCheckBox("add textures", 5, 80, \
                 135, 20)
            self.texturesCheckBox = self.noeWnd.getControlByIndex(index) 
            self.texturesCheckBox.setChecked(1)
            
            self.noeWnd.createStatic("uTile:", 72, 107, 70, 20)
            self.noeWnd.createStatic("vTile:", 74, 130, 70, 20)
            #            
            index = self.noeWnd.createEditBox(110, 105, 70, 20, None, 0)
            self.utileEdit = self.noeWnd.getControlByIndex(index) 
            self.utileEdit.setText(str(DEFAULT_UTILE))            
            index = self.noeWnd.createEditBox(110, 130, 70, 20, None, 0)
            self.vtileEdit = self.noeWnd.getControlByIndex(index)            
            self.vtileEdit.setText(str(DEFAULT_VTILE))
            
            self.noeWnd.createButton("Import", 190, 5, 80, 30, \
                 self.openOptionsButtonImport)
            self.noeWnd.createButton("Cancel", 190, 40, 80, 30, \
                 self.openOptionsButtonCancel)
            
            self.noeWnd.doModal()   
    
    
def rawLoadModel(data, mdlList):       
    #if noesis.optWasInvoked("-heightcoeff"):
    #    try: 
    #        hc = float(noesis.optGetArg("-heightcoeff"))
    #    except ValueError:
    #        hc = DEFAULT_HEIGHT_COEFF
        
    #    if hc <= 0 or hc > 1:       
    #        hc = DEFAULT_HEIGHT_COEFF
            
    #    heightmap = heightmapMesh(raw.heightsData, hc)
    #else:
    #    heightmap = heightmapMesh(raw.heightsData)
    
    openOptionsDialog = openOptionsDialogWindow()
    openOptionsDialog.create()

    if not openOptionsDialog.isCanceled: 
        raw = RAWFile(NoeBitStream(data))   
        raw.read()
               
        hmMesh = heightmapMesh(raw.heightsData, openOptionsDialog.options["HeightCoefficient"],
                                  openOptionsDialog.options["SandLevel"], openOptionsDialog.options["UTile"],
                                  openOptionsDialog.options["VTile"])
         
        hmMesh.create()
         
        ctx = rapi.rpgCreateContext()

        #noesis.logPopup()
        #startTime = time.time()   
 
        # transform heightmap to original view
        transMatrix = NoeMat43(((0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 0, 0)))
        rapi.rpgSetTransform(transMatrix)      
 
        for surface in heightmap.surfaces:
            if heightmap.textures:     
                rapi.rpgSetMaterial(surface.materialName)
    
            rapi.immBegin(noesis.RPGEO_TRIANGLE)
         
            for face in surface.faces:
                for vertex in face:
                    rapi.immUV2(vertex.uv)
                    rapi.immVertex3(vertex.pos) 
                
            rapi.immEnd()              
    
        #rapi.rpgOptimize()
        mdl = rapi.rpgConstructModelSlim()
        if heightmap.textures: 
            mdl.setModelMaterials(NoeModelMaterials(heightmap.textures, \
                heightmap.materials))
        mdlList.append(mdl)
   
  
    #timeTaken = time.time() - startTime
    #print("Total load time:", timeTaken, "seconds.")   
    #rapi.setPreviewOption("setAngOfs", "0 0 0")
    
    return 1   