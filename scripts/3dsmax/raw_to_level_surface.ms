/*
  Author: AlexKimov
  Version: 0.1
  Description: script combine all heightmaps into one to look like the same as one of the game's level surface
  Format: *.raw
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "lib/ms.ms"
filein "lib/raw/raw.ms"
filein "lib/raw/heightmap.ms"
filein "lib/raw/terrain.ms"
filein "lib/txr.ms"
filein "lib/res.ms"
filein "lib/max.ms"
filein "lib/dialogs.ms"
filein "lib/utils.ms"
filein "lib/settings.ms"
filein "lib/bitmap.ms"

struct dialogSettings
(
  rolloutWidth = 100,
  rolloutPos = [100, 100],
  rolloutStyle = #(#style_toolwindow, #style_sysmenu),   
  terrainFilename = #("terrain0.raw", "terrain1.raw", "terrain2.raw"),
  standTexture = #("sand_tex.bmp", "rock_tex.bmp"),
  texTexture = #("ter000.txr", "ter100.txr"),
  resTexture = #("ter000.txr", "ter100.txr"),  
  terrainPath = "",
  terrainSize = 256,
  rotationAngle = 90,
  texturedSurface = true, 
  heightCoeff = 0.1,
  texturesFolderName = "textures\\",
  texSource = 3, 
  path = "",  
  fn loadFromIni filename =
  (
    local sets = settings(this)
    sets.loadFromIniFile filename "LevelSurfaceRolloutDialog"
  ) 
)

struct dialogStrings
(
  rolloutTitle = "Import terrain files",
  openFolderCaption = "Open .raw files folder",  
  terrainSizeEditTitle = "Terrain size",
  rotationAngleEditTitle = "Angle",
  buttonCaption = "Import",
  texCheckBoxTitle  = "Textured",
  cantCreateDialog  = "Can't create ui dialog.",
  blendCheckBoxTitle = "Blended",  
  dialogStrings.radioButtonLabels = \
    ("Resource (.res)", "texture (.txr)", "stand. image"),  
  fn loadFromIni filename =
  (
    local sets = settings(this)
    sets.loadFromIniFile filename "LevelSurfaceRolloutDialog"
  )  
)

struct levelSurface
( 
  settings,
  strings,
  terrainMeshArray = #(),
  dialog = 
  (
    rollout dialog strings.rolloutTitle
    (
      local owner = if owner != undefined do owner
      local dialogSettings = if dialogSettings != undefined do dialogSettings 
      local dialogStrings = if dialogStrings != undefined do dialogStrings
      
      -- UI elements
      edittext edit_heightCoeff dialogStrings.heightCoeffEditTitle \
        text: dialogSettings.heightCoeff labelOnTop:true       
      edittext edit_terrainSize dialogStrings.terrainSizeEditTitle \
        text: dialogSettings.terrainSize labelOnTop:true       
      edittext edit_rotationAngle dialogStrings.rotationAngleEditTitle \
        text: dialogSettings.rotationAngle labelOnTop:true
      checkbox checkbox_textured dialogStrings.texCheckBoxTitle checked:true
      checkbox checkbox_blend dialogStrings.blendCheckBoxTitle checked:true       
      radiobuttons radiobtns_textureSource \
        labels:dialogStrings.radioButtonLabels default:3 
        
      button button_import dialogStrings.buttonCaption
      on button_import pressed do with undo off  
      (
        for dialogControl in this.controls do 
        (
          if classof dialogControl == EditTextControl then 
          if not dialogs.checkInputValue (dialogControl.text) then
          (
            case dialogControl.name of  
            (  
              edit_heightCoeff: dialogControl.text = dialogSettings.heightCoeff
              edit_terrainSize: dialogControl.text = dialogSettings.terrainSize
              edit_rotationAngle: dialogControl.text = dialogSettings.rotationAngle
            )    
          )  
        )    
   
        owner.importTerrainsToMesh \
          (converter.stringToInteger edit_heightCoeff.text) \
          (converter.stringToInteger edit_terrainSize.text) \ 
          (converter.stringToInteger edit_rotationAngle.text) \
          radiobuttons.state checkbox_textured.checked
      )        
    )    
  ),
  fn loadTerrainFile filename =
  (
    local raw = heightmapFile()
    raw.settings.getFromIniFile (path + settings.iniFile)
    raw.filename = filename
    raw.settings.zCoeff = settings.heightCoeff
    raw.settings.cellWidth = 1
    raw.settings.cellHeight = 1
    if raw.openFile "rb" != undefined then
    (
      if raw.readFile() then
        result = raw
      else
        result = undefined 
      raw.closeFile() 
      result      
    )
  ),
  fn createBitmapFromTexture filename source =
  (
    if source = 1 then
    (
      texture = txrFile()
      texture.filename = filename
      if texture.openFile() != undefined then
      (
        texture.readFile() 
        texture.closeFile()
      )   
    )
    else
    (
      resFile = resourceFile()
      if resFile.openFile() != undefined then
      (
        if resFile.readFile() then
          result = resFile
        resFile.closeFile()     
      )
      texture = resFile.loadTexture filename      
    ) 
    local data = rgba.unpack32 texture.imageData texture.masks    
    local textureBitmap = max.createBitmap data texture.width \
      texture.height texture.filename    
  ),
  fn createBitmapFromTextureFile filename =
  (
    local texture = loadTerrainTextureFile(filename) 
    bitmap = max.createBitmap texture.imageData texture.width texture.height \
      filename
    texture.closeFile()  
    bitmap
  ),  
  fn createTerrainMesh filename =
  (
    local terrain = loadTerrainFile filename
    if terrain != undefined then
    (
      local faceArray = heightmaps.generateFaces()     
      if settings.texturedSurface then
      (
        local idArray = heightmaps.generateIds terrain.vertArray faceArray
        local tvertArray = heightmaps.generateTVerts faceArray.count    
        terrainMesh = max.createTexturedMesh terrain.vertArray faceArray \
          idArray tvertArray (filenameFrompath filename) 
      )        
      else
        terrainMesh = max.createTexturedMesh terrain.vertArray faceArray \ 
          (filenameFrompath filename)
      if terrainMesh != undefined  then 
        append terrainMeshArray terrainMesh 
    )    
  ),
  fn existTerrainFiles path = 
  (
    local result = false 
    for name in settings.terrainFilename do
    (
      result = false
      if not doesFileExist (path + name) then 
        return result
      else 
        result = true   
    )
    result
  ), 
  fn openTerrainFiles =
  (     
    local result = true 
    if settings.terrainPath != undefined then
      result = existTerrainFiles settings.terrainPath
    else
    ( 
      settings.terrainPath = dialogs.openFolder settings.openFolderCaption 
      if settings.terrainPath == undefined then 
        result = false 
      else 
        result = true
    )    
  ),
  fn createTerrainMaterial =
  (
    result = undefined 
    if settings.texturedSurface then
    (
      local textureBitmap = #()
      case settings.textureSource of
      (       
        1: textures = settings.resTexture 
        2: textures = settings.standTexture 
        3: textures = settings.standTexture        
      )      
      local texturesPath = path + settings.texturesFolderName + "\\"
      if fileUtils.isFileExist (texturesPath + textures[1]) \
        and fileUtils.isFileExist (texturesPath + textures[2]) then
      (      
        progressStart "creating materials" 
        local progress = (100.0/textures.count as float)
        for i = 1 to textures.count do
        ( 
          if fileUtils.getFileExtenion(texturesPath + textures[i]) == ".txr" then
            bitmapImage = createBitmapFromTexture (texturesPath + textures[i])
          else  
            bitmapImage = max.openBitmapFile (texturesPath + textures[i])
          if bitmapImage == undefined then 
          (
            progressEnd()
            return result = undefined           
          )
          append textureBitmap bitmapImage
          progressUpdate progress*i          
        )          
        progressEnd()         
        terrainMaterial = max.createBitmapMultiMaterial textureBitmap
        result = terrainMaterial           
      ) 
      else 
      (
        result = undefined
      ) 
    )    
  ),
  fn createSurface =
  (
    progressStart "creating meshes"
    -- create base meshes
    local count = settings.terrainFilename.count
    local progress = (100.0/count as float)
    for i = 1 to count do
    (
      createTerrainMesh (settings.terrainPath + settings.terrainFilename[i])
      progressUpdate progress*i
    )   
    progressEnd() 
    
    if terrainMeshArray.count == 3 then
    (        
       -- load textures
      terrainMaterial = createTerrainMaterial()     
      
      local terrainMesh = terrainMeshArray[3] 
      -- assign textures to terrain2 mesh    
      if terrainMaterial  != undefined then max.addMaterialToMesh (terrainMesh) \
        (terrainMaterial)
    
      -- rotate mesh
      max.rotateMesh terrainMesh (eulerAngles 0 0 settings.rotationAngle)
      for i = 1 to 4 do
      (
        if i > 1 then
        (
          terrainMesh = max.copyMesh terrainMeshArray[3]
          append terrainMeshArray terrainMesh
        )         
        terrainMesh.name = "terrain2_" + i as string
        case i of
        (
          2: max.moveMesh terrainMesh [-settings.terrainSize, \
            -settings.terrainSize, 0] -- left
          3: max.moveMesh terrainMesh [settings.terrainSize, \
            -settings.terrainSize, 0]  -- right
          4: max.moveMesh terrainMesh [0, -2*settings.terrainSize, 0]  -- bottom   
        )
      )   
      -- position terrain0 parts
      terrainMesh = terrainMeshArray[1] 
      -- assign textures to terrain0 mesh    
      if terrainMaterial  != undefined then max.addMaterialToMesh (terrainMesh) \
        (terrainMaterial)    
      max.rotateMesh terrainMesh (eulerAngles 0 0 settings.rotationAngle)
      for i = 1 to 3 do
      (
        if i > 1 then
        (
          terrainMesh = max.copyMesh terrainMeshArray[1]  
          append terrainMeshArray terrainMesh 
        )     
        terrainMesh.name = "terrain0_" + i as string
        case i of
        (
          1: max.moveMesh terrainMesh [-settings.terrainSize, 0, 0] -- left top         
          2: max.moveMesh terrainMesh [settings.terrainSize, \
            -settings.terrainSize, 0]  -- center
          3: max.moveMesh terrainMesh [settings.terrainSize*2, \
            -settings.terrainSize*2, 0]  -- right bottom
        )
      )      
      -- position terrain1
      terrainMesh = terrainMeshArray[2] 
       -- assign textures to terrain1 mesh    
      if terrainMaterial  != undefined then max.addMaterialToMesh (terrainMesh) \
        (terrainMaterial)   
      max.rotateMesh terrainMesh (eulerAngles 0 0 settings.rotationAngle)
      for i = 1 to 2 do
      (
        if i == 2 then
        (
          terrainMesh = max.copyMesh terrainMeshArray[2]
          append terrainMeshArray terrainMesh 
        )         
        terrainMesh.name = "terrain1_"  + i as string
        case i of
        (
          -- left top
          1: max.moveMesh terrainMesh [-settings.terrainSize, 0, 0] 
          -- right bottom
          2: max.moveMesh terrainMesh [settings.terrainSize*2, \
              -settings.terrainSize*2, 0]  
        )
      )
      -- slice top-left mesh
      max.sliceMesh terrainMeshArray[1] [0.5, -0.5, 0] \
        [-settings.terrainSize/2 - settings.terrainSize, settings.terrainSize/2, 0]  
      -- slice right bottom mesh
      max.sliceMesh terrainMeshArray[8] [-0.5, 0.5, 0] \
        [settings.terrainSize/2, - settings.terrainSize/2 - settings.terrainSize, 0] 
      -- slice top-left mesh
      max.sliceMesh terrainMeshArray[2] [-0.5, 0.5, 0] \
        [-settings.terrainSize/2 - settings.terrainSize, settings.terrainSize/2, 0]
      -- right bottom
      max.sliceMesh terrainMeshArray[9] [0.5, -0.5, 0] \
        [settings.terrainSize/2, - settings.terrainSize/2 - settings.terrainSize, 0]
    
      -- TODO: attach meshes
    )
  ),
   fn importTerrainsToMesh heightCoeff terrainSize rotationAngle textureSource \
     isTextured  = 
  (
    settings.heightCoeff = heightCoeff
    settings.terrainSize = terrainSize
    settings.rotationAngle = rotationAngle
    settings.texturedSurface = isTextured 
    settings.texSource = textureSource
    if openTerrainFiles() then
      createSurface()
  ), 
  fn init =
  (
    if settings == undefined then 
      settings = dialogSettings() 
    if strings == undefined then 
      strings = dialogStrings()       
    dialog.owner = this  
    dialog.dialogSettings = settings  
    dialog.dialogStrings = strings    
    if not createDialog dialog width:settings.rolloutWidth pos:settings.rolloutPos \
      style:settings.rolloutStyle then
    then 
      dialogs.showMessage dialogStrings.cantCreateDialog                 
  ),
  on create do init()  
)

fn main = 
(
  currrentPath = sysinfo.currentdir + "\\" 
  settings = settings()
  settings.getFromIniFile (currrentPath + "settings.ini")
  settings.terrainPath = "C:\Games\King\ENV\\"
  settings.terrainFilename = #("terrain0.raw", "terrain1.raw", "terrain2.raw")
  settings.texture = #("sand_tex.bmp", "rock_tex.bmp")
  settings.texturesFolderName = "textures"
  settings.iniFile = "settings.ini"
  levelSurface = levelSurface settings:settings path:currrentPath
)

main()