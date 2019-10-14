/*
  Description:
  3ds max objects
*/                                           

bi = Python.Import "python/image.py"

struct rgbMasks
(
  redMask,
  greenMask,
  blueMask,
  alphaMask
)

struct rgba
(
  fn unpack8To24 imageData =
  (
    local textureData = #() 
    for pixel8 in imageData do
    (
      local bitmapPixel = color pixel8 pixel8 pixel8
      append textureData bitmapPixel     
    )
  ),
  fn unpackTo32 imageData bitMasks =
  (
    local Table4 = #(0, 17, 34, 51, 68, 86, 102, 119, 136, 153, 170, \
    181, 204, 221, 238, 255)
    local Table5 = #(0, 8, 16, 25, 33, 41, 49, 58, 66, 74, 82, 90, 99, 107, \
      115,  123, 132, 140, 148, 156, 165, 173, 181, 189, 197, 206, 214, 222,\ 
      230, 239, 247, 255)
    local Table6 = #(0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 45, 49, 53, 57, \
      61,  65, 69, 73, 77, 81, 85, 89, 93, 97, 101, 105, 109, 113, 117, 121, \
      125, 130, 134, 138, 142, 146, 150, 154, 158, 162, 166, 170, 174, 178, \
      182, 186, 190, 194, 198, 202, 206, 210, 215, 219, 223, 227, 231, 235, \
      239, 243, 247, 251, 255) 
    local textureData = #()     
    for pixel16 in imageData do
    (
      local bitmapPixel = color 0 0 0 0 
      -- RGBA 565
      case bitMasks.redMask of
      (
        31744:
        (
          bitmapPixel.r = Table5[(bit.shift (bit.and pixel16 bitMasks.redMask) -11) + 1]  
          bitmapPixel.g = Table6[(bit.shift (bit.and pixel16 bitMasks.greenMask) -5) + 1]
          bitmapPixel.b = Table5[(bit.and pixel16 bitMasks.blueMask) + 1]             
        )
        61440:
        (
          bitmapPixel.r = Table4[(bit.shift (bit.and pixel16 bitMasks.redMask) -12) + 1]       
          bitmapPixel.g = Table4[(bit.shift (bit.and pixel16 bitMasks.greenMask) -8) + 1]
          bitmapPixel.b = Table4[(bit.shift (bit.and pixel16 bitMasks.blueMask)  -4) + 1] 
          bitmapPixel.a = Table4[(bit.and pixel16 bitMasks.alphaMask) + 1];         
        )
        default:
        (
          bitmapPixel.r = Table5[(bit.and pixel16 bitMasks.redMask) + 1];  
          bitmapPixel.g = Table5[(bit.shift (bit.and pixel16 bitMasks.greenMask) -5) + 1]; 
          bitmapPixel.b = Table5[(bit.shift (bit.and pixel16 bitMasks.blueMask) -10) + 1]; 
          bitmapPixel.a = Table1[(bit.shift (bit.and pixel16 bitMasks.alphaMask) -15) + 1];       
        )
      ) 
      append textureData bitmapPixel     
    )     
    textureData
    print textureData[1]
  )
);

rgba = rgba()