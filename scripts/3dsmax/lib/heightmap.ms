/*
  Author: AlexKimov
  Version: 0.1
  Description:
*/

struct heightmapUtils
(
  size = 257,
  uTile = 10,
  vTile = 10,
  groundLevel = 10,
  /*
    face array starts with lower left corner (heightmap grid) with clockwise order
  */
  fn generateFaces =
  (
    local faceIndex = 1
    local col = 0
    local faceArray = #()
    for i = 0 to size*(size - 2) do 
	(		
      append faceArray [faceIndex + 1, faceIndex + size, faceIndex]
      append faceArray [faceIndex + 1, faceIndex + size + 1, faceIndex + size]
      col += 1
      faceIndex += 1
      if col > (size - 2) then 
	  (
	    col = 0
        faceIndex += 1
      ) 
    )
    result = faceArray
  ),
  /*
    vertex array fills from back to top from left to right, to transform 
    coordinates into 3dsmax ones
  */  
  fn heightsToVertArray heightArray zCoeff cellWidth cellHeight =
  (
    local col = 0
    local row = size - 1
    vertArray = #()
    for point in heightArray do  
	(	
      append vertArray [(col*cellWidth as float), \
        ((size - row - 1)*cellHeight as float), \
        (z*zCoeff as float)]                 
      col += 1 
      if col > (size - 1) then 
	  (
        row -= 1
        col = 0 
      ) 
    ) 
    result = vertArray    
  ),
  /*
    material ids: 
      1 - sand texture by default
      2 - rock texture by default
      3 - blended rock and sand textures
  */  
  fn generateIds vertArray faceArray isBlended = 
  (
    local idArray = #()
    for i = 1 to faceArray.count do
    (
      local indexes = #()
      append indexes faceArray[i].x
      append indexes faceArray[i].y
      append indexes faceArray[i].z    
      Z = 0
      for index in indexes do
      (
        if Z < vertArray[index].z then 
          z = vertArray[index].z
      )

      if Z >= groundLevel then
      (
        if isBlended then
        (
          if Z < groundLevel + 0.1 then
            append idArray 3
          else          
            append idArray 2         
        )
        else
          append idArray 2 
      )    
      else
          append idArray 1        
    )        
    result = idArray  
  ),  
  /*
    UV coordinates
  */   
  fn generateTVerts = 
  (
    local tvertArray = #()
    local u = (uTile/(size - 1) as float)
    local v = (vTile/(size - 1) as float) 
        
    for row = 0 to (size - 1) do
      for col = 0 to (size - 1) do 
        append tvertArray [(u*col as float), (v*row as float), 0]               
    result = tvertArray    
  ),
   /*
    water level in .raw is about (0.38..0.41)*height
  */  
  fn getWaterLevel height = 
  (
    result = 0.4*height
  )   
)

heightmaps = heightmapUtils()