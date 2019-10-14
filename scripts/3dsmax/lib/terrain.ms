/*
  Author: AlexKimov
  Version: 0.1
  Description: 
*/

filein "max.ms"
filein "heightmap.ms" 

struct terrainSettings
(
  texturedSurface = true,
  texBlending = false,
  trees = false,
  bushes = false,
  water = false     
)

struct position
(
  coord = [0, 0, 0],
  rot = (EulerAngles 0 0 90) 
)

struct scatterOptions
(
  type = 1, -- scatter by height
  heightMax = 0,
  heightMin = 0
)

struct terrainMesh
(
  settings,
  heightmapMesh,
  treeMesh,
  bushMesh,
  waterMesh,
  texture = #(),
  
  fn createHeightmapMesh heightmap bitmap nme =
  (
    local vertexArray = heightmapUtils.heightsToVertArray heightArray \
      settings.zCoeff settings.cellWidth settings.cellHeight
    local faceArray = heightmapUtils.generateFaces()  
    if isTextured then
    (   
      local materialIDs = heightmapUtils.generateIds vertexArray faceArray \
        isTexBlended 
      local tverts = heightmapUtils.generateTVerts          
      result = max.createTexturedMesh vertexArray faceArray \
          materialIDs tverts nme     
    )
    if isTextured == unsupplied or isTextured == false then
      result = max.createMesh getVertexArray() getFaceArray() nme      
  ),
  fn createTerrainObjectMesh size pos bmap nme =
  (
    msh = max.createPlaneMesh size pos.coord nme
    if msh != undefined then 
    (
      max.addBitmapToMesh msh bmap
      max.rotateMesh msh pos.angle
      result = msh 
    )    
  ),
  fn scatterMsh msh distribMesh settings duplicates:30 =
  (
    if settings == unsupplied then
      settings = scatterOptions()
    local newNodeArr = #()
    dimensions = max.distribMesh msh
    local vertexArray = max.getMeshVerts msh
    local vArray = for vertex in vertexArray where vertex.z <= settings.height \
      collect vertex    
    for i = 1 to duplicates do
    (
      --if settings.type == 1 then            
      local newPos = getVert vArray (random 1 vArray.numVerts)     
      max.cloneMesh msh newPos &newNodeArr 
      local newInst = newNodeArr[1]				
      local scaleRand = (random 0.01 1.0)
      newInst.scale = [scaleRand, scaleRand, scaleRand]         
    )
  ),  
  fn createFromHeightmap heightmap =
  (
    progressStart "creating meshes"
    progressUpdate 15  
    local faceArray = heightmaps.generateFaces()
    if isTextured then 
    (
      local texturesPath = settings.path + settings.texturesFolderName 
      if not fileUtils.isFileExist (texturesPath + settings.texture[1]) \
        or not fileUtils.isFileExist (texturesPath + settings.texture[2]) then
        texturesPath = getSavePath "Open folder with texture files" 
      progressUpdate 30      
      msh = createHeightmapMesh heightmap
      progressUpdate 45
      if msh != undefined then
      (
        local sandTexture = max.openBitmapFromFile \
          (texturesPath + settings.texture[1])
        local rockTexture = max.openBitmapFromFile \
          (texturesPath + settings.texture[2])

        if sandTexture != undefined and rockTexture != undefined then
        (     
          local textureBitmap = #()             
          append textureBitmap sandTexture      
          append textureBitmap rockTexture
          progressUpdate 75          
          local terrainMaterial = max.createBitmapMultiMaterial textureBitmap \
            texBlending
          max.addMaterialToMesh (msh) (terrainMaterial) 
          progressUpdate 80              
        )  
            
        if treesOn then
        (
          local treeBitmap = max.openBitmapFromFile \
            (texturesPath + settings.texture[3])
          if treeBitmap != undefined then
          (
            local pos = position()
            pos.coord = [0, 0] 
            pos.rot = (EulerAngles 0 0 90)        
            treeMesh = createTerrainObjectMesh [0.1, 0.1] pos treeBitmap "tree" 
            op = scatterOptions()
            op.heightMax = 10 
            op.heightMin = 10            
            scatterMesh treeMesh msh options:op
          )            
        )
        
        progressUpdate 85               
        if bushesOn then
        (
          local bushBitmap = max.openBitmapFromFile \
            (texturesPath + settings.texture[4]) 
          if bushBitmap != undefined then 
          (    
            local pos = position()
            pos.coord = [0, 0] 
            pos.rot = (EulerAngles 0 0 90)             
            bushMesh = createTerrainObjectMesh [0.1, 0.1] pos bushBitmap "bush" 
            op = scatterOptions()
            op.heightMax = 10 
            op.heightMin = 10             
            scatterMesh bushMesh msh options:op         
          )            
        )
        
        progressUpdate 90  
        if waterOn then
        (  
          local waterBitmap = max.openBitmapFromFile \
            (texturesPath + settings.texture[5])             
          dimensions = max.getMeshDimension msh     
          local size = [dimensions[1], dimensions[2]]
          local pos = position()
          pos.coord = [msh.pos.x, msh.pos.y, raw.getWaterLevel()]        
          waterMesh = createTerrainObjectMesh size pos waterBitmap "water"          
        )
        progressUpdate 95             
      )          
    )    
    else  
    (        
      progressUpdate 50
      msh = raw.createMesh()
    )  
    
    progressUpdate 100             
    if msh != undefined then 
      redrawViews()
    progressEnd()   
  ),
  fn init =
  (
    settings = terrainSettings()
  ),
  on create do init()  
)