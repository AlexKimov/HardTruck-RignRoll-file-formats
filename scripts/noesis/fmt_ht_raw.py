from inc_noesis import *
import time
import os 


def registerNoesisTypes():
    handle = noesis.register("Hard Truck 2 heightmap", ".raw")
    noesis.setHandlerTypeCheck(handle, rawCheckType)
    noesis.setHandlerLoadModel(handle, rawLoadModel)
    #noesis.setHandlerWriteModel(handle, rawWriteModel)
    
    noesis.addOption(handle, "-heightcoeff", "height coefficient (0..1)", \
        noesis.OPTFLAG_WANTARG)  
    noesis.addOption(handle, "-sealevel", "sea level (0..255)", \
        noesis.OPTFLAG_WANTARG)         
    return 1
 

DEFAULT_HEIGHT_COEFF = 0.22
DEFAULT_SEA_LEVEL = 90
DEFAULT_HEIGHTMAP_SIZE = 257
DEFAULT_UTILE = 1  
DEFAULT_VTILE = 1 
 
class RAWFile:
    def __init__(self, reader):
        self.reader = reader
        self.heightsData = []
     
    def loadVertsData(self, filereader):   
        vertInRowCount = DEFAULT_HEIGHTMAP_SIZE
        filesize = vertInRowCount * vertInRowCount
    
        for row in range(vertInRowCount):
            line = bytearray() 
            for col in range(vertInRowCount):             
                line.append(filereader.readUByte())          
                filereader.seek(1, NOESEEK_REL) # skip one bit
            self.heightsData.append(line)
            
        return 1
    
    def loadData(self):   
        self.loadVertsData(self.reader)  
        
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
    def __init__(self, heightsData, heightCoeff = DEFAULT_HEIGHT_COEFF, \
            seaLevel = DEFAULT_SEA_LEVEL):
        self.heights = heightsData            
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
        
        utile = 1/(heightmapSize - 1)
        vtile = 1/(heightmapSize - 1)
        
        gridStepX = 1
        gridStepY = 1
        
        # building faces (triangles)
        # starting from top bottom and back row by row
        for row in range(0, heightmapSize - 2):
            for col in range(0, heightmapSize - 1):
                # first triangle 
                vertex1 = faceVertex()
                vertex1.pos = (gridStepX*(col + 1), gridStepY*(row), \
                    self.heights[row][col + 1] * \
                    self.heightCoeff)
                vertex1.uv = (utile*col, vtile*row) 
                 
                vertex2 = faceVertex()  
                vertex2.pos = (gridStepX*col, gridStepY*(row), \
                    self.heights[row][col] * self.heightCoeff)
                vertex2.uv = (utile*col, vtile*row)

                vertex3 = faceVertex()                     
                vertex3.pos = (gridStepX*col, gridStepY*(row + 1), \
                    self.heights[row + 1][col] * \
                    self.heightCoeff)
                vertex3.uv = (utile*col, vtile*row)
                          
                self.addFace(vertex1, vertex2, vertex3)  
                
                # second triangle
                vertex1 = faceVertex()                
                vertex1.pos = (gridStepX*(col + 1), gridStepY*(row + 1), \
                    self.heights[row + 1][col + 1] * \
                    self.heightCoeff)
                vertex1.uv = (utile*col, vtile*row)
                
                vertex2 = faceVertex()    
                vertex2.pos = (gridStepX*(col + 1), gridStepY*(row), \
                    self.heights[row][col + 1] * \
                    self.heightCoeff)
                vertex2.uv = (utile*col, vtile*row)
                
                vertex3 = faceVertex()    
                vertex3.pos = (gridStepX*col, gridStepY*(row + 1), \
                    self.heights[row + 1][col] * \
                    self.heightCoeff)
                vertex3.uv = (utile*col, vtile*row)
                
                self.addFace(vertex1, vertex2, vertex3) 
       
    def create(self): 
        self.buildFaces()
        self.loadTextures()

    
def rawCheckType(data):

	return 1
 

def rawWriteModel(mdl, filewriter):
    #heightmapSize = DEFAULT_HEIGHTMAP_SIZE
    #count = 0
    #size = heightmapSize * heightmapSize
    
    #print("mesh count: ", len(mdl.meshes))
    
    
    #for mesh in mdl.meshes:
        #print("pos count: ", len(mesh.positions))
        #for vcmp in mesh.positions:         
            #bytes = int(vcmp[2]).to_bytes(1, byteorder='little')
            #bytes += bytes
            #filewriter.writeBytes(bytes) 
                
            #if count == size:
                #break  

            #count += 1
                      
    return 1  
            
def rawLoadModel(data, mdlList):   
    raw = RAWFile(NoeBitStream(data))
   
    raw.loadData()
    
    if noesis.optWasInvoked("-heightcoeff"):
        try: 
            hc = float(noesis.optGetArg("-heightcoeff"))
        except ValueError:
            hc = DEFAULT_HEIGHT_COEFF
        
        if hc <= 0 or hc > 1:       
            hc = DEFAULT_HEIGHT_COEFF
            
        heightmap = heightmapMesh(raw.heightsData, hc)
    else:
        heightmap = heightmapMesh(raw.heightsData)
    
    heightmap.create()  
 
    ctx = rapi.rpgCreateContext()

    #noesis.logPopup()
    #startTime = time.time()   
 
    # rotating heightmap 90 left
    transMatrix = NoeMat43( ((0, 1, 0), (1, 0, 0), (0, 0, 1), (0, 0, 0)) )    
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