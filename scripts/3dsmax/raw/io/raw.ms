/*
  Description:
  Heightmap (.raw) file definition
*/

struct Heightmapfile 
(
  vertArray = #(),
  faceArray = #(),
  filename, filestream,
  pointsInLine = 257, 
  pointSizeinBytes = 2, 
  zCoeff = 0.1, 
  cellWidth = 1,
  cellHeight = 1,
  fn getPointCount = (pointsInLine*pointsInLine),  
  fn writeFile vertArray boundPoint = 
  (
    count = getPointCount()
	print count
    for i = 1 to count do 
    (  
	  value = 256*vertArray[i].z/boundPoint[1].z
	  WriteByte filestream value
	  WriteByte filestream value 
	)	
	print ".raw file saved"
  ),
  fn readFile =
  (
    -- read verts
    x = 0
    y = 0
    for i = 0 to pointsInLine*pointsInLine - 1 do 
	(	
      fseek filestream (i*pointSizeinBytes) #seek_set
      z = ReadByte filestream #unsigned	
 
      append vertArray [x*cellWidth, y*cellHeight, z*zCoeff as float] 
      x += 1 
      if x > 256 then 
	  (
        y += 1
        x = 0 
      ) 
    )  
	-- add faces
    fi = 1
    col = 0
    for i = 0 to pointsInLine*255 do 
	(		
      append faceArray [fi + 1, fi + pointsInLine, fi]
      append faceArray [fi + 1, fi + pointsInLine + 1, fi + pointsInLine]
      col += 1
      fi += 1
      if col > 255 then 
	  (
	    col = 0
        fi += 1
      ) 
    )	
  ),
  fn openFile mode = 
  (
	if mode  == "rb" then
    (
      filename = getOpenFileName \
      caption: "Open heightmap file" \
      types: "Heightmap (*.raw)|*.raw"
      filestream = fopen filename mode
    )	
	else
	(
      filename = getSaveFileName \
      caption: "Open heightmap file" \
      types: "Heightmap (*.raw)|*.raw"
      filestream = fopen filename mode	
	)
  ),
  fn closeFile = 
  (
    fclose filestream
  )
)