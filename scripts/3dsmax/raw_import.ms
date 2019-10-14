/*
  Author: AlexKimov
  Version: 0.31
  Description: Hard Truck 2 heightmap (.raw) file importer
  Format: *.raw
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "lib/ms.ms"
filein "lib/ini.ms"
filein "lib/max.ms"
filein "lib/utils.ms"
filein "lib/raw.ms"
filein "lib/heightmap.ms"
filein "lib/terrain.ms"
filein "lib/settings.ms"
filein "lib/dialogs.ms"

struct importDialogSettings
(
  extendedUI = true,
  rolloutWidth = 100,
  rolloutPos = [100, 100],
  rolloutStyle = #(#style_toolwindow, #style_sysmenu), 
  heightCoeffEditText = "0.1",
  cellWidthEditText = "1",
  
  treeCopysEditText = "30",
  bushCopysEditText = "30",
  treeHeightEditText = "0.1",  
  bushHeightEditText = "0.1",
  waterLevelEditText = "10", 

  cellHeightEditText = "1",
  
  texturedSurface = true,
  texBlending = false,
  treesOn = false,
  bushesOn = false,
  waterOn = false,
  aiOn = false,  
  textures = #("sand_tex.bmp", "rock_tex.bmp", "tree_tex.bmp", "bush_tex.bmp" \
    "water_tex.bmp"), 
  texturesFolderName = "textures\\",
  path = "",  
  fn loadFromIni filename =
  (
    local settings = settings(this)
    settings.loadFromIniFile filename "ImportRolloutDialog"
  ) 
)

struct importDialogStrings
(
  rolloutTitle = "Import .raw file", 
  heightCoeffEditTitle = "Height coeff.:",
  cellWidthEditTitle = "Grid cell width:",
  cellHeightEditTitle = "Grid cell height:",
  scatterGroupCaption = "Scatter",
  blendCheckBoxTitle = "isTexBlended",  
  treeCopysEditTitle = "Tree copys",
  bushCopysEditTitle = "Bush copys",  
  heightEditTitle = "Height", 
  objectsGroupCaption = "Objects",
  levelEditTitle = "Level",
  texturesGroupCaption = " Texture List", 
  chooseButtonCaption = "Choose",   
  optionsButtonCaption = "options",
  addButtonCaption = "Add",  
  aiCheckBoxTitle  = "Ai paths",
  fnCheckBoxTitle = "filename:",
  triCheckBoxTitle = "triangles:",
  facesCheckBoxTitle = "faces:",
  sbCheckBoxTitle = "Skybox",
  labelText = "click to open file",
  buttonCaption = "Import",
  buttonUpdateCaption = "Update",  
  texCheckBoxTitle  = "Textured", 
  cantCreateDialog  = "Can't create ui dialog.",  
  fn loadFromIni filename =
  (
    local settings = settings(this)
    settings.loadFromIniFile filename "Strings"
  ) 
)

struct importDialog
(
  dialogSettings,
  dialogStrings,
  terrainMesh,
  dialog =
  (
    rollout dialog dialogStrings.rolloutTitle
    (
      local owner = if owner != undefined do owner
      local settings = if settings != undefined do settings 
      local strings = if strings != undefined do strings
      
      -- UI elements
      --width:200 height:683
      
      if settings.extendedUI then
      (
	    groupBox grp_heightmap "Heightmap" pos:[10, 65] width:179 height:106 
	    editText edit_heightCoeff strings.heightCoeffEditTitle \
          pos:[21, 84] width:98 height:22 text: settings.heightCoeffEditText
	    editText edit_cellWidth strings.cellWidthEditTitle \ 
          pos:[37, 111] width:82 height:22 text: settings.cellWidthEditText
	    editText edit_cellHeight strings.cellHeightEditTitle \
          pos:[33, 139] width:86 height:22 text: settings.cellHeightEditText
	    groupBox grp_textures "Textures" pos:[10, 176] width:179 height:258 
        
	    checkbox checkbox_textured strings.texCheckBoxTitle pos:[21, 189] \
          width:83 height:30
	    checkbox checkbox_trees strings.treesCheckBoxTitle pos:[21, 455] \
          width:80 height:27 
	    checkbox checkbox_bushes strings.bushesCheckBoxTitle pos:[98, 453] \
          width:75 height:30 
	    checkbox checkbox_texBlending strings.blendCheckBoxTitle \
          pos:[98, 189] width:82 height:30 
	    checkbox checkbox_water strings.waterCheckBoxTitle pos:[20, 482] \
          width:93 height:22
	    groupBox grp_scatter strings.scatterGroupCaption pos:[10, 563] \
          width:179 height:81 
          
	    editText edit_treecopys strings.treeCopysEditTitle pos:[26, 583] \
          width:82 height:22 text: strings.treeCopysEditText
	    editText edit_bushcopys strings.bushCopysEditTitle pos:[21, 611] \
          width:87 height:22 text: strings.bushCopysEditText
	    editText edit_treeheight strings.heightEditTitle pos:[117, 583] \
          width:62 height:22 text: strings.treeHeightEditText
	    editText edit_bushheight strings.heightEditTitle pos:[117, 611] \
          width:62 height:22 text: strings.bushHeightEditText
          
	    groupBox grp_objs strings.objectsGroupCaption pos:[10, 440] \
          width:180 height:118 
	    editText edit_waterLevel strings.levelEditTitle pos:[98, 482] \
          width:80 height:22 text: strings.waterLevelEditText
	    dropDownList ddlist_textures strings.texturesGroupCaption \
          pos:[21, 217] width:104 height:40 items: settings.textures  
	    bitmap bmp_view "" pos:[21,266] width:157 height:157 
	    button button_choose strings.chooseButtonCaption pos:[131, 234] \
          width:47 height:25 
	    button button_opts strings.optionsButtonCaption pos:[130, 84] \
          width:48 height:22 
	    button button_add strings.addButtonCaption pos:[99,510] \
          width:80 height:22 
	    checkbox checkbox_ai strings.aiCheckBoxTitle pos:[20, 507] \
          width:71 height:22 
	    label lbl_filename strings.fnCheckBoxTitle pos:[12, 8] \
          width:44 height:22 
	    label lbl_triangules strings.triCheckBoxTitle pos:[12, 26] \
          width:66 height:22 
	    label lbl_faces strings.facesCheckBoxTitle pos:[11, 44] \
          width:39 height:18 
	    checkbox checkbox_skybox strings.sbCheckBoxTitle pos:[20, 536] \
          width:67 height:11 
        
	    button button_update strings.buttonUpdateCaption pos:[10, 652] \
          width:86 height:22 enabled:false toolTip:"Update" 
	    button button_import strings.buttonCaption pos:[103, 652] \
          width:86 height:22      
      )
      else
      (
        edittext edit_heightCoeff strings.heightCoeffEditTitle \
          text: settings.heightCoeffEditText labelOnTop:true       
        edittext edit_cellWidth strings.cellWidthEditTitle \
          text: settings.cellWidthEditText labelOnTop:true         
        edittext edit_cellHeight strings.cellHeightEditTitle \
          text: settings.cellHeightEditText labelOnTop:true 
        checkbox checkbox_textured strings.texCheckBoxTitle \
          checked:settings.texturedSurface  
        checkbox checkbox_texBlending strings.blendCheckBoxTitle \
          checked:texBlending
        checkbox checkbox_trees strings.treesCheckBoxTitle checked:trees
        checkbox checkbox_bushes strings.bushesCheckBoxTitle checked:bushes
        checkbox checkbox_water strings.waterCheckBoxTitle checked:water      
        label lbl_click strings.labelText
        button button_import strings.buttonCaption
      )    
      
      on dropDownList selected item do
      (
        bmp_view.fileName = settings.path + settings.texturesFolderName + \
          settings.selected
      )
      
      on button_choose pressed do
      (
        owner.getNewTexture ddlist_textures.selection 
      ) 

      on button_opts pressed do
      (
        
      )
      
      on button_add pressed do
      (
        
      )
      
      on button_update pressed do with undo off 
      (
        
      )
      
      on button_import pressed do with undo off 
      (
        -- check input values
        for dialogControl in this.controls do 
        (
          if classof dialogControl == EditTextControl then 
          if not dialogs.checkInputValue (dialogControl.text) then
          (
            case dialogControl.name of  
            (  
              edit_heightCoeff: dialogControl.text = settings.heightCoeff
              edit_cellWidth: dialogControl.text = settings.cellWidth
              edit_cellHeight: dialogControl.text = settings.cellHeight
            )   
            if settings.extendedUI then
              case dialogControl.name of  
              (  
                edit_treecopys: dialogControl.text = settings.treeCopysEditText
                edit_bushcopys: dialogControl.text = settings.bushCopysEditText
                edit_treeheight: dialogControl.text = settings.treeHeightEditText
                edit_bushheight: dialogControl.text = settings.bushHeightEditText 
                edit_waterLevel: dialogControl.text = settings.waterLevelEditText                 
              )              
          )  
        )     
        settings.texturedSurface = checkbox_textured.checked 
        settings.texBlending = checkbox_texBlending.checked 
        settings.treesOn = checkbox_trees.checked 
        settings.bushesOn = checkbox_bushes.checked
        settings.waterOn = checkbox_water.checked
        settings.aiOn = checkbox_ai.checked         
        if settings.extendedUI then 
        (  
          
        )        
        owner.importRawFileToMesh()
      )  
    )
  )
  fn importRawFileToMesh zCoeff cellWidth cellHeight =
  (
    local raw = heightmapFile()
    raw.settings.getFromIniFile (dialogSettings.path + "settings.ini")
    if raw.openFile("rb") != undefined then
    (
      raw.settings.zCoeff = dialogSettings.zCoeff
      raw.settings.cellWidth = dialogSettings.cellWidth
      raw.settings.cellHeight = dialogSettings.cellHeight
      if raw.readFile() then with redraw off()
      (
        terrainMesh = terrainMesh()
        terrainMesh.settings.texturedSurface = dialogSettings.texturedSurface
        terrainMesh.settings.texBlending = dialogSettings.texBlending
        terrainMesh.settings.treesOn = dialogSettings.trees
        terrainMesh.settings.bushesOn = dialogSettings.bushes
        terrainMesh.settings.waterOn = dialogSettings.water 
        terrainMesh.texture = dialogSettings.texture
        terrainMesh.createFromHeightmap raw.heightArray
      )
      raw.closeFile()
    )
  ),
  fn close = try (destroyDialog dialog) catch(),
  fn init = 
  (
    if dialogSettings == undefined then
      dialogSettings = importDialogSettings()
    if dialogStrings == undefined then  
      dialogStrings = importDialogStrings()
    dialog.owner = this
    dialog.settings = dialogSettings
    dialog.strings = dialogStrings
    if dialogSettings.extendedUI then
      result = createDialog dialog width:283 height:683 \
      pos:dialogSettings.rolloutPos \
      style:dialogSettings.rolloutStyle
     else
      result = createDialog dialog width:dialogSettings.rolloutwidth \
      pos:dialogSettings.rolloutPos \
      style:dialogSettings.rolloutStyle     
    if not result then 
      dialogs.showMessage dialogStrings.cantCreateDialog            
  ),
  on create do init()
)

fn main = 
(
  currrentPath = fileUtils.getCurrentPath(getThisScriptFilename())
  textureFolder = "textures\\"
  
  settings = importDialogSettings()
  iniFileName = "settings.ini"
  settings.getFromIni(currrentPath + iniFileName)
  settings.texturesFolderName = textureFolder
  settings.path = currrentPath
  strings = importDialogStrings()
  iniFileName = "strings.ini"
  strings.getFromIni(currrentPath + iniFileName)
  
  importUI = importDialog dialogSettings:settings dialogStrings:strings
)

main()