/*
  Description:
  Hard Truck 1/2 texture import
*/

struct rgbMasks
(
  red,
  green,
  blue,
  alpha
)

struct txrFile 
(
  height,
  width,
  filename, filestream,
  imageData,
  masks = rgbMasks red:63488 green:2016 blue:31 alpha:0, -- rgb565
  fn getMasksPos =
  ( 
    fseek filestream 26
    pos = ReadInt filestream #unsigned	
	pos	
  ),
  fn readHeader =
  (
    fseek filestream 12
	width = ReadShort filestream #unsigned	
	fseek filestream 2
	height = ReadShort filestream #unsigned	
	fseek filestream 4
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
  fn readImageData =
  (
    pixelCount = height*width
    for i = 1 to pixelCount do
	(
      pixel = ReadShort filestream #unsigned
	  fseek filestream 2
	  append imageData pixel
	)
  ), 
  fn readFile =
  ( 
    readHeader()
	readImageData()
	readMasks()
  ),  
  fn openFile = 
  (
	if filename == "" then	  
      filename = getOpenFileName \
      caption: "Open heightmap file" \
      types: "Heightmap (*.raw)|*.raw"
    filestream = fopen filename "rb"
  ),
  fn closeFile = 
  (
    fclose filestream
  )
)