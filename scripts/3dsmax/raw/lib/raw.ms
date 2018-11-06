/*
  Author:
  Version: 0.11
  Description: Heightmap (.raw) file definition
*/

filein "lib/filestream.ms"
filein "lib/ini.ms"

struct heightmapSettings
(
  heightMethod = 1,
  pointsInLine = 257, 
  pointSizeinBytes = 2, 
  openFileCaption = "Open heightmap file",
  saveFileCaption = "Save heightmap file",
  types = "Heightmap (*.raw)|*.raw",
  iniFile = "settings.ini",
  fn getFromIniFile iniFileName =
  (
  	local filename = sysInfo.currentdir + "\\" + iniFileName
    strNames = #("openFileCaption", "saveFileCaption", "types")
	strName = ""
    ini.filename = iniFile 
	if doesFileExist filename then
      ini.filename = filename
	if doesFileExist ini.filename then 
	(
	  local strValue
      names = getPropNames this
	  for name in names do
	  (
	    strName = name as string
	    if ini.isKeyExist "RAW"	strName then
		(
		  if findItem strNames strName > 0 then
		  (
		    strValue = ini.getValue "RAW" strName
		    if strValue != "" then
	          setProperty this name strValue
	      )	
          else
          (
		    intValue = ini.getIntegerValue "RAW" strName
		    if intValue > 0 then
	          setProperty this name intValue		  
		  )		  
		)
	  )
    )
  )
)

struct heightmapFile 
(
  vertArray = #(),
  faceArray = #(),
  filename = "", filestream,
  settings,
  zCoeff = 0.1, 
  cellWidth = 1,
  cellHeight = 1,
  fn getPointCount = 
  (
    settings.pointsInLine*settings.pointsInLine
  ),  
  fn writeFile vertArray boundPoint = 
  (
    count = getPointCount()
	try
	(
	  local n = 0
	  local k = settings.pointsInLine - 1
      for i = 1 to count do 
      (  
	    value = 255*vertArray[k*settings.pointsInLine + n + 1].z/boundPoint[1].z
	    WriteByte filestream value
	    WriteByte filestream value
        n += 1		
        if n > (settings.pointsInLine - 1) then 
	    (
          k -= 1
          n = 0 
        ) 		
	  )
	)
    catch	
    (
      messageBox ("ERROR. Can't write to the file " + filename + ".")
    )
  ),
  fn readFile =
  (
    -- read verts
    local x = 0
    local y = settings.pointsInLine - 1
	local z 
    local i = 0
	try
	(
      for i = 0 to settings.pointsInLine*settings.pointsInLine - 1 do  
	  (	
        fseek filestream ((settings.pointsInLine*y + x)*settings.pointSizeinBytes) #seek_set
        z = ReadByte filestream #unsigned	
        append vertArray [x*cellWidth, (settings.pointsInLine - y - 1)*cellHeight, z*zCoeff as float] 
        x += 1 
        if x > (settings.pointsInLine - 1) then 
	    (
          y -= 1
          x = 0 
        ) 
      ) 
    )	  
    catch	
    (
      messageBox ("ERROR. Can't read from the file " + filename + ".")
    )	
	print "File " + filename + " was opened."	
	-- add faces
    local fi = 1
    local col = 0
    for i = 0 to settings.pointsInLine*(settings.pointsInLine - 2) do 
	(		
      append faceArray [fi + 1, fi + settings.pointsInLine, fi]
      append faceArray [fi + 1, fi + settings.pointsInLine + 1, fi + settings.pointsInLine]
      col += 1
      fi += 1
      if col > (settings.pointsInLine - 2) then 
	  (
	    col = 0
        fi += 1
      ) 
    )	
  ),
  fn openFile mode = 
  (
	if mode == "rb" then
    (
	  if filename == "" then	  
        filename = getOpenFileName \
        caption: settings.openFileCaption \
        types: settings.types
    )	
	else
	(
	  if filename == "" then	 
        filename = getSaveFileName \
        caption: settings.saveFileCaption \
        types: settings.types
	)
	if filename != undefined then
      filestream = fopen filename mode
  ),
  fn closeFile = 
  (
    fclose filestream
  ),
  fn init = 
  (
    if settings == undefined then
	(
      local rawSettings = heightmapSettings()
      rawSettings.getFromIniFile("settings.ini")
      settings = rawSettings	  
	)
  ),
  on create do init()  
)