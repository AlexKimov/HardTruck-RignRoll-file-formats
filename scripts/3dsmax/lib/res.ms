/*
  Author:
  Version: 0.11
  Description: Heightmap (.raw) file definition
*/

filein "filestream.ms"
filein "ini.ms"
filein "dialogs.ms"
filein "txr.ms"

struct resourceFile
(
  textureArray = #(),
  filename = "", 
  filestream,
  fn openFile =
  (
    filestream = dialogs.openFileDialog filename mode  
  ),
  fn readFile = 
  (

  ),
  fn init()
)