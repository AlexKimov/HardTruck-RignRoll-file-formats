/*
  Description:
  3ds max objects
*/

struct Max3ds
(
  VisualStyle = #Shaded,
  fn getSelestedBoundPoint =
  (
    boundPoint = #()
    append boundPoint selection[1].max
	append boundPoint selection[1].min
	boundPoint
  ),
  fn Init =
  (
	-- set viewport mod
    VP = NitrousGraphicsManager.GetActiveViewportSetting()
    VP.VisualStyleMode = VisualStyle
  ),
  fn getSelestedVert count =
  (
    vertArray = #()
    msh = selection[1]
    for i = 1 to count do 
      append vertArray (getVert msh i)
	vertArray
  ), 
  fn createMesh vertArray faceArray name =
  (
    Init()
    msh = mesh vertices:vertArray faces:faceArray
    msh.name="Heightmap: " + name   
  )
)