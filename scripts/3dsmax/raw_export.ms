/*
  Author: AlexKimov
  Version: 0.1
  Description: Hard Truck 2 heightmap (.raw) file export script
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "lib/ms.ms"
filein "lib/raw.ms"
filein "lib/max.ms"
filein "lib/settings.ms"
filein "lib/dialogs.ms"
filein "lib/utils.ms"

struct exportDialogSettings
(
  mainSection = "MAIN",
  lang = "ENG",
  fn loadFromIni filename =
  (
    local sets = settings(this)
    sets.loadFromIniFile filename mainSection
  )  
)

struct exportDialogStrings
(
  iniLang = "ENG",
  heighthmapFileSaved = "Heighthmap file %s was saved.",
  meshNotSelected = "Heightmap mesh isn't selected.",
  errorZeroHeight = "Mesh %s has zero height.",
  buttonCaption = "Export",
  rolloutTitle = "Export heightmap",
  radioNumObjLabels = #("first", "all"),
  numExportedObjsCaption = "Export selection",  
  exportSettingsText = "Settings",
  errorMeshSize = "Mesh: Wrong number of vertices. Must be equal %i.",
  exportGroupCaption = "Export settings",
  exportLangText = "Language",
  langCaption = "Choose language",
  langLabels = #("RU", "EN"),
  langButtonCaption = "Set",
  langGroupCaption = "Lang settings",
  errorObjectType = "Error: Wrong object type.",
  directionCheckBoxCaption = "change direction",
  flipXCheckBoxCaption = "flip x",
  flipYCheckBoxCaption = "flip y",
  fn loadFromIni filename =
  (
    local strings = settings(this)
    strings.loadFromIniFile filename iniLang
  )
)

struct exportDialog
(
  strings,
  langSettingsRollout =
  (
    rollout langSettingsRollout strings.exportLangText
    (
      local owner = if owner != undefined do owner 
      
      groupBox export_group owner.strings.langGroupCaption pos:[4, 2] \
        width:175 height:80     
      radiobuttons radio_numberObj owner.strings.langCaption \
        labels:owner.strings.langLabels pos:[40, 20] default:2 
      button button_setlang strings.langButtonCaption width:110 enabled:false
      
      on button_setlang pressed do
      (
        --
      )         
    )
  ),   
  exportSettingsRollout =
  (
    rollout exportSettingsRollout strings.exportSettingsText
    (
      local owner = if owner != undefined do owner 
      
      groupBox export_group owner.strings.exportGroupCaption pos:[4, 2] \
        width:175 height:115
      radiobuttons radio_numberObj owner.strings.numExportedObjsCaption \
        labels:owner.strings.radioNumObjLabels pos:[35, 20]  
        
      checkbox checkbox_direction owner.strings.directionCheckBoxCaption \
        pos:[35, 55]
      checkbox checkbox_flipX owner.strings.flipXCheckBoxCaption pos:[35, 70]
      checkbox checkbox_flipY owner.strings.flipYCheckBoxCaption pos:[85, 70]
      
      button button_export strings.buttonCaption width:110 pos:[35, 90]
      
      on button_export pressed do
      (
        flipX = checkbox_flipX.checked
        flipY = checkbox_flipY.checked 
          
        flip = 0
 
        if flipX and flipY then
          flip = 3
        else 
        (
          if flipX then 
            flip = 1
          if flipY then
            flip = 2
        )   
      
        owner.exportMeshToRaw checkbox_direction.checked flip      
      )    
    )
  ),  
  dialog = 
  (
    rollout dialog strings.rolloutTitle
    (
      subrollout subroll_container "container" height:260 width:196 pos:[2, 2]
    )    
  ),  
  fn exportMeshToRaw direction flip =
  (
    local minHeight = 0.0001 -- mesh height expected/taken to be lowest
    local numbMesh = selection.count 
    if numbMesh > 0 then
    (
      /*
        Hard Truck 2 uses 3 heightmap files, it combines them into a single big 
        terrain located at Greystone (Алмазный) location.
      */      
      if numbMesh > 3 then numbMesh = 3
      for i = 1 to numbMesh do 
      (
        heightmapMesh = selection[i]  
        if classof selection[i] != Editable_Mesh then
          heightmapMesh = convertToMesh heightmapMesh
        
        if heightmapMesh == undefined then
        (
          dialogs.showMessage (formattedprint raw.filename \
            format:strings.errorObjectType)
        )
        else
        (
          raw = heightmapFile()     
          if raw.openFile "wb" != undefined then
          (
	        local vertexArray = max.getMeshVerts heightmapMesh            
            if raw.getPointCount() == (vertexArray.count) then
            (
              local height = (max.getMeshDimension heightmapMesh)[3]
              if (height > minHeight) then
              (
                if raw.writeFile vertexArray height direction flip then
                  dialogs.showMessage (formattedprint raw.filename \
                    format:strings.heighthmapFileSaved)
              )      
              else      
                dialogs.showMessage (formattedprint heightmapMesh.name \
                  format:strings.errorZeroHeight)                    
            )
            else
              dialogs.showMessage (formattedprint (raw.getPointCount()) \
                format:strings.errorMeshSize) 
            
            raw.closeFile()                 
          )
        )         
      )        
    )
    else
      dialogs.showMessage strings.meshNotSelected    
  ),
  fn init =
  (
    if strings == undefined then
      strings = exportDialogStrings()
      
    exportSettingsRollout.owner = this
    langSettingsRollout.owner = this   
    
    createDialog dialog width:200 pos:mouse.screenpos \
      style:#(#style_toolwindow, #style_sysmenu) 
    AddSubRollout dialog.subroll_container langSettingsRollout
    AddSubRollout dialog.subroll_container exportSettingsRollout      
  ),
  on create do init()
)

fn main = 
(
  currentPath = fileUtils.getCurrentPath(getThisScriptFilename())

  iniFileName = "raw_export_settings.ini"  
  sets = exportDialogSettings() 
  sets.loadFromIni (currentPath + iniFileName)

  iniFileName = "raw_export_strings.ini"  
  strings = exportDialogStrings sets.lang  
  strings.loadFromIni (currentPath + iniFileName)
   
  exportRaw = exportDialog strings 
)

main()