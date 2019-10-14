/*
  Author: AlexKimov
  Version: 0.1
  Description: 
  Format: *.b3d
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "lib/ms.ms"
filein "lib/b3D.ms"

struct settings
(
  
  
)

struct strings
(
  
  
)

struct dataImportUI
( 
  settings,
  strings,
  dialog = 
  (
    rollout dialog settings.rolloutTitle
    (
      local owner = if owner != undefined do owner
      local dialogSettings = if dialogSettings != undefined do dialogSettings 
      local dialogStrings = if dialogStrings != undefined do dialogStrings
      button button_import strings.buttonImportCaption
    )
  ),
  fn importFromFile =
  (
    
  ),
  fn init = 
  (
  
  ),
  on create do init()
)  