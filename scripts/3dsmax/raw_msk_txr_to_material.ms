/*
  Author: AlexKimov
  Version: 0.1
*/

filein "lib/ms.ms"
filein "lib/max.ms"
filein "lib/txr.ms"
filein "lib/raw.ms"
filein "lib/bitmap.ms"
filein "lib/utils.ms"
filein "lib/dialogs.ms"
 
struct textureMaterial
(
  filename,
  fn loadTextureFile filename =
  (
    local texture = txrFile()
    texture.filename = filename
    if texture.openFile() != undefined then
    (
      if texture.readFile() then
        result = texture
      else
        result = undefined
    )
  ), 
  fn createBitmapFromMask =
  (
    
  ),  
  fn createBitmapFromTexture =
  (  
    local texture = loadTextureFile()
    if texture != undefined then
    (    
      local textureBitmap = max.createBitmap texture.unpackedData texture.width \
        texture.height texture.filename
      texture.closeFile()  
      textureBitmap
    )
  ),
  fn createBitmapFromRaw =
  (  
    local raw = heightmapFile()
    raw.filename = filename
    raw.settings.zCoeff = 1
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
  fn createMaterial =
  (
    local mesh = selection[1]
    if mesh != undefined then
    (
      local extension = fileUtils.getFileExtension
      if extension == ".txr" then   
        bitmap = createBitmapFromMask()
      if extension == ".msk" then  
        bitmap = createBitmapFromTexture()       
      if extension == ".raw" then 
        bitmap = createBitmapFromRaw()
 
      if bitmap != undefined then
        max.addBitmapToMesh mesh bitmap
      else
        dialogs.showMessage ""      
    ) 
    else    
      dialogs.showMessage ""    
  )
)  

fn main =
(
  texMat = textureMaterial()
  texMat.filename = sysInfo.currentdir + "\\" + "textures\\BackService.txr"
  texMat.createMaterial()
)

main()