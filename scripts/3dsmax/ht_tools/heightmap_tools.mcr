/*
  Author: AlexKimov
  Version: 0.1
  Description: Hard Truck 2 heightmap tools
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

macroScript HEIGHTMAP_TOOLS
category: "Game file import"
tooltip: "Hard Truck 2 heightmap tools"
buttontext: "Heightmap tools"
icon: #("ht_icon", 1)
autoUndoEnabled:false
(
  struct toolsDialog
  (
    title = "Heightmap tools",
    width = 100,
    pos = [100, 100],
    style = #(#style_titlebar, #style_border, #style_sysmenu, #style_minimizebox),
    fn importRawFile = 
    (
  	  include "raw_import.ms"
    ),
    fn exportRawFile = 
    (
  	  include "raw_export.ms"
    ),
    fn rawToSurface  = 
    (
  	  include "raw_to_level_surface.ms"
    ),	
    dialog =
    (
      rollout dialog title
      (
	    local owner = if owner != undefined do owner
	    button button_importRaw "Import RAW"
	    button button_exportRaw "Export RAW"
  	    button button_rawToLevelSurface "Import terrain"	  
  	    on button_importRaw pressed do owner.importRawFile 
  	    on button_exportRaw pressed do owner.exportRawFile 
   	    on button_rawToLevelSurface pressed do owner.rawToSurface 
      )
    ),
    fn show = createDialog dialog width:width pos:pos style:style,
    fn close = try (destroyDialog dialog) catch(),
    on create do dialog.owner = this
  )
  
  htToolsUI = toolsDialog()
  htToolsUI.show() 
)