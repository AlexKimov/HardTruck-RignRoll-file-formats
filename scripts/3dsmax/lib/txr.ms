/*
  Description:
  Hard Truck 1/2 texture import
*/

filein "bitmap.ms"
filein "dialogs.ms"
filein "settings.ms"

struct strings
(
  caption = " ",
  types = " "
)

struct txrFile 
( 
  strings,
  height,
  width,
  filename, 
  filestream,
  imageData,
  masks = rgbMasks redMask:63488 greenMask:2016 blueMask:31 alphaMask:0, -- rgb565
  fn getMasksPos =
  ( 
    fseek filestream 26 #seek_set 
    local pos = ReadLong filestream #unsigned	
  ),
  fn readHeader =
  (
    fseek filestream 12 #seek_cur
	width = ReadShort filestream #unsigned	
	height = ReadShort filestream #unsigned	
	fseek filestream 14 #seek_cur
  ), 
  fn readMasks =
  (
    local pos = getMasksPos()
	fseek filestream (pos + 8) #seek_set   
    masks.redMask = ReadLong filestream #unsigned	
    masks.greenMask = ReadLong filestream #unsigned
    masks.blueMask = ReadLong filestream #unsigned	
    masks.alphaMask = ReadLong filestream #unsigned	
  ),  
  fn unpackData =
  (
    if imageData != undefined 
    (
      start = timeStamp()
      result = rgba.unpack32 imageData masks
      end = timeStamp()
      format "Processing took % seconds\n" ((end - start) / 1000.0)
    )    
  ),
  fn readImageData =
  (
    pixelCount = height*width
    for i = 1 to pixelCount do
	(
      pixel = ReadShort filestream #unsigned
	  append imageData pixel
	)
  ), 
  fn readFile =
  ( 
    try
    (
      readHeader()
    )
    catch
    (
      dialogs.showMessage (formattedprint filename \
        format:strings.)
    ) 

    try
    (    
	  readImageData()
    )  
    catch
    (
      dialogs.showMessage (formattedprint filename \
        format:strings.)
    ) 
 
    try
    (    
	  readMasks()
    )  
    catch
    (
      dialogs.showMessage (formattedprint filename \
        format:strings.masksError)
    )     
  ),  
  fn openFile = 
  (
    dialogs.caption = strings.caption
    dialogs.types = strings.types
	filestream = dialogs.openFileDialog filename mode
  ),
  fn closeFile = 
  (
    fclose filestream
  )
)