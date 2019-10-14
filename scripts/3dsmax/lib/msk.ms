/*
  Description:
  Hard Truck 1/2 mask texture files import
*/

filein "bitmap.ms"
filein "dialogs.ms"

struct mskFile 
(
  type,
  height,
  width,
  filename, filestream,
  imageData,
  palette,
  masks = rgbMasks red:63488 green:2016 blue:31 alpha:0, -- rgb565
  fn getMasksPos =
  ( 
    fseek filestream 26
    pos = ReadInt filestream #unsigned	
	pos	
  ),
  fn readHeader =
  (     
    type = readChars filestream 4
	width = ReadShort filestream #unsigned	
	fseek filestream 2
	height = ReadShort filestream #unsigned	
  ),
  fn readPalette =
  (
    if type == "MS16" then
      fseek filestream 768
    else
      for i = 1 to 768 do
      (
        paletteColor = color 0 0 0
        paletteColor.red = ReadShort filestream
        paletteColor.green = ReadShort filestream
        paletteColor.blue = ReadShort filestream
        append palette paletteColor
      )  
  ),   
  fn readMasks =
  (
    pos = getMasksPos()
	fseek(pos)
    masks.red = ReadInt filestream #unsigned	
	fseek filestream 4
    masks.green = ReadInt filestream #unsigned	
	fseek filestream 4
    masks.blue = ReadInt filestream #unsigned	
	fseek filestream 4
    masks.alpha = ReadInt filestream #unsigned	
	fseek filestream 4	
  ),  
  fn readMask16 = 
  (
    if b <= 127 then
    (
      for i = 1 to b do
	    append imageData 0      
    )
    else
    (
      for i = 1 to b do
	    append imageData ReadShort filestream #unsigned     
    )  
  ),
  fn readMask8 = 
  (
    if b <= 127 then
    (
      for i = 1 to b do
	    append imageData 0      
    )
    else
    (
      for i = 1 to b do
	    append imageData ReadByte filestream #unsigned     
    )
  ),
  fn readImageData =
  (
    pixelCount = height*width
    try
    (
      while not eof filestream
      (
        b = readByte filestream
        if b == 80 then
        ( 
        
          if (readChars filestream 4)
          readMasks()
        )
        if type == "MS16" then
          readMask16()
        else 
          readMask8()      
      )
      result = true
    )
    catch	
    (
      messageBox ("ERROR. Can't read file " + filename + ".")  
      result = false      
    )
  ), 
  fn readFile =
  ( 
    readHeader()
    readPalette()    
	readImageData()
  ),  
  fn openFile = 
  (
	filestream = dialogs.openFileDialog filename mode
  ),
  fn closeFile = 
  (
    fclose filestream
  )
)