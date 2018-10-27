/*
  Author: AlexKimov
  Version: 0.1
  Description: Hard Truck 2 heightmap (.raw) file importer
  Format: *.raw
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "io/raw.ms"
filein "io/max.ms"

clearlistener() 

struct importDialog
(
  title = "Import .raw file",
  width = 100,
  pos = [100, 100],
  style = #(#style_titlebar, #style_border, #style_sysmenu, #style_minimizebox),
  fn importRawFile zCoeff cellWidth cellHeight =
  (
    raw = Heightmapfile()
    raw.openFile "rb"
	raw.zCoeff = zCoeff
	raw.cellWidth = cellWidth
	raw.cellHeight = cellHeight
    raw.readFile()
    raw.closeFile()
    Max = Max3ds()
    Max.createMesh raw.vertArray raw.faceArray (filenameFromPath raw.filename)	
    redrawViews()	
  ),
  dialog =
  (
    rollout dialog title
    (
	  local owner = if owner != undefined do owner
	  edittext heightCoeff "Height coeff.:" text: "0.1" labelOnTop:true 
	  edittext cellWidth "Grid cell size (X):" text: "1" labelOnTop:true 
	  edittext cellHeight "Grid cell size (Y):" text: "1" labelOnTop:true 	  
	  label lbl_click "click to open file"
	  button button_import "Import"
	  on button_import pressed do owner.importRawFile (heightCoeff.text as float) (cellWidth.text as float) (cellHeight.text as float)
    )
  ),
  fn show = createDialog dialog width:width pos:pos style:style,
  fn close = try (destroyDialog dialog) catch(),
  on create do dialog.owner = this
)

ImportUI = importDialog()
ImportUI.show()




