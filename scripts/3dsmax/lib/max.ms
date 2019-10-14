/*
  Description:
  3ds max objects
*/

filein "dialogs.ms"

struct maxStrings 
(
  lang = "Eng",
  errorVertNumber = "Error. Number of vertexes of the mesh is less than %d.",
  fn loadFromIni filename =
  (
    local strings = settings(this)
    strings.loadFromIniFile filename lang
  )
)

struct max3ds
(
  strings,
  VisualStyle = #Shaded,
  fn getBoundPoints mesh =
  (
    boundPoint = #()
    append boundPoint mesh.max
	append boundPoint mesh.min
	boundPoint
  ),
  fn init =
  (
    if strings == undefined then
      strings = maxStrings() 
	-- set viewport mod
    VP = NitrousGraphicsManager.GetActiveViewportSetting()
    VP.VisualStyleMode = VisualStyle
  ), 
  fn getMeshDimension msh =
  (
    meshDimensions = msh.max - msh.min
  ),
  fn getMeshVertCount msh =
  (
    result = getNumVerts msh 
  ),
  fn getMeshVerts mesh =
  (
    vertArray = #()
    for i = 1 to mesh.numVerts do 
      append vertArray (getVert mesh i)
  	result = vertArray
  ),
  fn createPlaneMesh size pos name =
  (
    vertArray = #([0, 0, 0], [size.x, 0, 0], [0, size.y, 0], [size.x, size.y, 0])
    faceArray = #([1, 2, 3], [2, 4, 3])
    idArray = #(1, 1)
    tvertArray = #([0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]) 
    msh = max.createTexturedMesh vertArray faceArray idArray tvertArray name
    if msh != undefined then
    (
      msh.pos = pos
      result = msh
    )
  ),  
  fn createMesh vertArray faceArray name =
  (
    try
	(
      msh = mesh vertices:vertArray faces:faceArray
      if name != unsupplied then
        msh.name = name 
      result = msh		
	)
	catch 
	(
	  messageBox ("ERROR. Can't create mesh: " + name + ".")
    )  	
  ), 
  fn createTexturedMesh vertArray faceArray idArray tvertArray name =
  (
    try
	(        
      if idArray == unsupplied then
        msh = mesh vertices:vertArray faces:faceArray tverts:tvertArray
      else      
        msh = mesh vertices:vertArray faces:faceArray materialIDS:idArray \
          tverts:tvertArray
    ) 
	catch 
	(
	  messageBox ("ERROR. Can't create mesh: " + name + ".")
      return undefined
    )      
    buildTVFaces msh.mesh
    for i = 1 to msh.mesh.numfaces do 
      (setTVFace msh.mesh i (getFace msh.mesh i)) 
    if name != unsupplied then      
      msh.name = name 
    result = msh			
  ),
  fn cloneMesh msh pos nodes =
  (
    maxOps.CloneNodes msh offset:pos expandHierarchy:false cloneType:#copy \
      newNodes:&nodes 
  ),
  fn moveMesh msh pos = 
  (
    move msh pos
  ),
  fn rotateMesh msh angles =
  (
    rotate msh angles
  ),
  fn copyMesh msh =
  (
    mshCopy = copy msh
	mshCopy
  ),
  fn attachMesh srcMesh dstMesh =
  (
    meshop.attach srcMesh dstMesh
  ),
  fn sliceMesh msh planeNormal planePos =
  (
  	local offset = dot planeNormal (planePos - (msh.pos * inverse msh.transform * msh.objecttransform))
  	meshop.slice msh #all planeNormal offset delete:true
  	update msh
  ),
  fn createBitmapMaterial bitmapImage =
  (
    local mat = standardMaterial diffuseMap:(bitmaptexture bitmap:bitmapImage) \
      showInViewport:true
  ),
  fn createBitmapBlendMaterial bitmapImageArray =
  (  
    blendmat = blend
    blendmat.map1 = standardMaterial \
      diffuseMap:(bitmaptexture bitmap:bitmapImageArray[1]) showInViewport:true
    blendmat.map2 = standardMaterial \
      diffuseMap:(bitmaptexture bitmap:bitmapImageArray[2]) showInViewport:true 
    blendmat.mask = gradient  
    result = blendmat    
  ),  
  fn createBitmapMultiMaterial bitmapImageArray isTexBlended =
  (  
    if isTexBlended then
      numsubs = bitmapImageArray.count + 1
    else
      numsubs = bitmapImageArray.count
    multimat = multimaterial numsubs:numsubs
    for i = 1 to bitmapImageArray.count do
      multimat[i] = standardMaterial \
      diffuseMap:(bitmaptexture bitmap:bitmapImageArray[i]) showInViewport:true
    if isTexBlended != unsupplied and isTexBlended then
      multimat[multimat.count + 1] = createBitmapBlendMaterial bitmapImageArray
    result = multimat  
  ), 
  fn addMaterialToMesh msh mat =
  (
  	msh.material = mat
  ),  
  fn addBitmapToMesh msh bitmapImage =
  (
  	msh.material = standardMaterial diffuseMap:(bitmaptexture bitmap:bitmapImage) showInViewport:true
  ),
  fn openBitmapFile filename =
  (
    try
    (
      openBitMap filename
    )  
    catch(
      messageBox ("Can't open bitmap file " + filename + ".")
      result = undefined
    )  
  ),
  fn createBitmap imageData imageWidth imageHeight filename =
  (
  	b = bitmap imageWidth imageHeight color:white 
	b.filename = filename + ".bmp"
    for line = 0 to (imageHeight - 1) do
    (
      row = for col = (line*imageWidth + 1) to (line + 1)*imageWidth collect
      (
        imageData[col]
      )
      setPixels b [0, line] row
    )       
    save b    
	b
  ),
  fn createHelperPoint name transformMatrix:0 =
  (
    hpoint = point
    hpoint.name = name
    if transformMatrix != unsupplied then
      hpoint.transform = transformMatrix
  ),
  on create do init()
)

max = max3ds()