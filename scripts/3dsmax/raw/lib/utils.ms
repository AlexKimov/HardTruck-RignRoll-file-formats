/*
  Author: AlexKimov
  Description: 
*/

struct converter (
  fn stringToPoint2 str = 
  (
    elements = filterstring str "[,]"
	if elements.count > 0 then
	(
	  try
      (	  
        first = elements[1] as integer
        second = elements[2] as integer
	  ) 
	  catch 
	  (
	    messageBox "Error. Can't convert: " + str + " to Point2 value"
	  )
      pointTwo = [first, second]
	)
	else
	(
	  --messageBox "Error. Can't convert: " + str + " to Point2 value"
	  [0, 0]
	)	  
  ),
  fn stringToInteger str = 
  (
    try
    (	  
      str as integer
    )
    catch 
	(
	  --messageBox "Error. Can't convert: " + str + " to integer value"
	  -1
	)
  ),
  fn stringToFloat str = 
  (
    try
    (	  
      str as float
	)  
    catch 
	(
	  --messageBox "Error. Can't convert: " + str + " to float value"
	  -1
	)	
  ),  
  fn stringToArray str = 
  (
    array = #()
    elements = filterstring str "(,)"
	if elements.count > 0 then
	  for element in elements do
        append array (element as name)
   	array  
  )
)

converter = converter()