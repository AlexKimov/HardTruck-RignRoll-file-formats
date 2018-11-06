/*
  Author: AlexKimov
  Version: 0.1
  Description: script combine all heightmaps into one to look like the same as one of the game's level surface
  Format: *.raw
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "lib/ms.ms"
filein "lib/raw.ms"
filein "lib/max.ms"
filein "lib/txr.ms"

clearlistener()

struct levelSurface
(
  terrainPath,
  terrainSize = 256,
  rotationAngle = 90,
  terrainFilenames = #(),
  terrainMeshArray = #(),
  fn loadTerrainFile filename =
  (
    local heightmap = Heightmapfile()
    heightmap.filename = filename
    heightmap.openFile "rb"
    heightmap.readFile()
    heightmap
  ),
  fn loadTerrainTextureFile filename =
  (
    local texture = txrFile()
    texture.filename = filename
    texture.openFile
    texture.readFile()
    texture
  ), 
  fn createBitmapFromTextureFile filename =
  (
    local texture = loadTerrainTextureFile(filename) 
    bitmap = max.createBitmap texture.imageData texture.width texture.height filename
	texture.closeFile()  
	bitmap
  ),  
  fn createTerrainMesh filename =
  (
    local terrain = loadTerrainFile(filename) 
    terrainMesh = max.createMesh terrain.vertArray terrain.faceArray (filenameFrompath filename)
	append terrainMeshArray terrainMesh
	terrain.closeFile()  
  ),
  fn existTerrainFiles path = 
  (
  	local result = false 
    for name in terrainFilenames do
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
    if terrainPath == undefined then
      terrainPath = getSavePath()
	  
	if terrainPath != undefined then
	(
	  terrainPath += "\\" 
	  existTerrainFiles terrainPath
	)
	else
      false	
  ),
  fn createSurface =
  (
    -- create
    local count = terrainFilenames.count
    for i = 1 to count do
    (
	  createTerrainMesh (terrainPath + terrainFilenames[i])
	)
    -- position terrain2
    local terrainMesh = terrainMeshArray[3]
	max.rotateMesh terrainMesh (eulerAngles 0 0 rotationAngle)
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
        2: max.moveMesh terrainMesh [-terrainSize, -terrainSize, 0] -- left
        3: max.moveMesh terrainMesh [terrainSize, -terrainSize, 0]  -- right
        4: max.moveMesh terrainMesh [0, -2*terrainSize, 0]  -- bottom	
      )
    ) 	

    -- position terrain0
    terrainMesh = terrainMeshArray[1] 
	max.rotateMesh terrainMesh (eulerAngles 0 0 rotationAngle)
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
        1: max.moveMesh terrainMesh [-terrainSize, 0, 0] -- left top		 
        2: max.moveMesh terrainMesh [terrainSize, -terrainSize, 0]  -- center
        3: max.moveMesh terrainMesh [terrainSize*2, -terrainSize*2, 0]  -- right bottom
      )
    )	
	
    -- position terrain1
    terrainMesh = terrainMeshArray[2] 
	max.rotateMesh terrainMesh (eulerAngles 0 0 rotationAngle)
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
        1: -- left top
		(
		  max.moveMesh terrainMesh [-terrainSize, 0, 0] 
		) 
        2: -- right bottom
		(
		  max.moveMesh terrainMesh [terrainSize*2, -terrainSize*2, 0]  
		)
      )
    )

	-- slice top-left mesh
	max.sliceMesh terrainMeshArray[1] [0.5, -0.5, 0] \
	  [-terrainSize/2 - terrainSize, terrainSize/2, 0]	
	-- slice right bottom mesh
	max.sliceMesh terrainMeshArray[8] [-0.5, 0.5, 0] \
	  [terrainSize/2, - terrainSize/2 - terrainSize, 0]	
	-- slice top-left mesh
	max.sliceMesh terrainMeshArray[2] [-0.5, 0.5, 0] \
	  [-terrainSize/2 - terrainSize, terrainSize/2, 0]
	-- right bottom
	max.sliceMesh terrainMeshArray[9] [0.5, -0.5, 0] \
	  [terrainSize/2, - terrainSize/2 - terrainSize, 0]
	
	-- attach terrains
	--for i = 1 to terrainMeshArray.count
	 -- if i != 7 do
	   -- max.attachMesh terrainMeshArray[7] terrainMeshArray[i]
  )  
)

levelSurface = levelSurface()
levelSurface.terrainPath = "C:\Games\King\ENV"
levelSurface.terrainFilenames = #("terrain0.raw", "terrain1.raw", "terrain2.raw")
if levelSurface.openTerrainFiles() then
  levelSurface.createSurface()