/*
  Author:
  Version: 0.11
  Description: Heightmap (.raw) file definition
*/

--filein "lib/filestream.ms"
filein "lib/ini.ms"
filein "lib/dialogs.ms"
filein "lib/heightmap.ms"

/*
  zCoeff - height adjustment coefficient, 0.2..0.25 seems to be fine
  cellWidth, cellHeight - heightmap grid cell size
  pointsInLine - heightmap size 257x257 points
  pointBytes - 2 bytes for each point in .raw file (first byte  = second byte)
*/

struct heightmapSettings
(
  zCoeff = 1, 
  cellWidth = 1,
  cellHeight = 1,
  pointsInLine = 257, 
  pointBytes = 2,
  fn loadFromIni filename =
  (
    local settings = settings(this)
    settings.loadFromIniFile filename "ImportRolloutDialog"
  ) 
)

struct heightmapStrings
(
  lang = "Eng",
  openFileCaption = "Open heightmap file",
  saveFileCaption = "Save heightmap file",
  types = "Heightmap (*.raw)|*.raw",
  errorWriteFile = "Error. Can't write to the file %s.",
  errorReadFile = "Error. Can't read from the file %s.",
  cantOpenFile = "Error. Can't open file.", 
  errorZValue = "Error: Mesh height value must be nonzero.",  
  fn loadFromIni filename =
  (
    local settings = settings(this)
    settings.loadFromIniFile filename lang
  ) 
)

struct heightmapFile
(
  heightArray = #(),
  filename = "", 
  filestream,
  settings,
  strings,
  fn getPointCount = 
  (
    result = settings.pointsInLine*settings.pointsInLine
  ),   
  fn writeFile vertArray zHeight changeDirection flip = 
  (
    if zHeight == 0 then
    (
      dialogs.showMessage (formattedprint filename format:strings.errorZValue)  
      return false 
    )  
         
    heightCoeff = 255/zHeight as float
    count = getPointCount()    
    
    stepRow = stepCol = 1    
    if changeDirection then
    (
      stepRow = settings.pointsInLine
      startRow = 0
      endRow = count - settings.pointsInLine
      startCol = 1
      endCol = settings.pointsInLine
    ) 
    else
    (
      startRow = 1
      endRow = settings.pointsInLine 
      startCol = 1
      endCol = settings.pointsInLine          
    )    
  
    if flip == 3 then
    (
      stepRow = -stepRow
      stepCol = -stepCol
      swap startRow endRow
      swap startCol endCol      
    )  
 
    if flip == 1 then
    (      
      stepRow = -stepRow
      swap startRow endRow
    )  

    if flip == 2 then
    (
      stepCol = -stepCol     
      swap startCol endCol      
    )
    
    try
	(   
     for row = startRow to endRow by stepRow do 
        for col = startCol to endCol by stepCol do
        (   
          if changeDirection then        
	        z = heightCoeff*vertArray[row + col].z
          else 
            z = heightCoeff*vertArray[row*col].z          
	      WriteByte filestream (z as integer) --#signed
	      WriteByte filestream (z as integer) --#signed
        )          
      result = true
	)
    catch	
    (
      dialogs.showMessage (formattedprint filename format:strings.errorWriteFile)  
      result = false      
    )    
  ),
  fn readFile =
  (
    -- Every second byte in .raw file is the same as the first one
    pointsInLine = settings.pointsInLine
    count = settings.pointBytes
	try
	(
      for row = 0 to pointsInLine - 1 do  
        for col = 0 to pointsInLine - 1 do
        (
          fseek filestream (pointsInLine*row + col)*count #seek_set
          height = ReadByte filestream #unsigned	
          append heightArray (height as float)                        
        )
      result = true
    )	  
    catch	
    (
      dialogs.showMessage (formattedprint filename format:strings.errorReadFile)
      result = false
    )	
  ),
  fn openFile mode = 
  (
    dialogs.types = strings.types
    if mode == "rb" then
      dialogs.caption = strings.openFileCaption
    else
      dialogs.caption = strings.saveFileCaption    
      
    filestream = dialogs.openFileDialog mode
    if filestream != undefined then
    (
      filename = dialogs.filename
      result = filestream 
    )  
  ),
  fn closeFile = 
  (
    fclose filestream
  ),
  fn init = 
  (
    if settings == undefined then
      settings = heightmapSettings()
    if strings == undefined then
      strings = heightmapStrings()       
  ),
  on create do init()  
)