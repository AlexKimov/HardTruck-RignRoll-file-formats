/*
  Description:
  3ds max objects
*/

struct max3ds
(
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
	-- set viewport mod
    VP = NitrousGraphicsManager.GetActiveViewportSetting()
    VP.VisualStyleMode = VisualStyle
  ),
  fn getMeshVerts mesh count =
  (
    vertArray = #()
    for i = 1 to count do 
      append vertArray (getVert mesh i)
	vertArray
  ), 
  fn createMesh vertArray faceArray name =
  (
    try
	(
      msh = mesh vertices:vertArray faces:faceArray
      msh.name = name 
      result = msh		
	)
	catch 
	(
	  messageBox ("ERROR. Can't create mesh: " + name + ".")
    )  	
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
  fn addBitmapToMesh msh bitmapImage =
  (
  	msh.material = standardMaterial diffuseMap:bitmapImage showInViewport:true
  ),  
  fn createBitmap imageData width height filename =
  (
  	b = bitmap width height color:white 
	b.filename = filename
	setPixels b [0, 0] imageData
	result = b
  ),
  on create do init()
)

max = max3ds()