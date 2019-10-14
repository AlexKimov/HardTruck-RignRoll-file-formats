/*
  Author:
  Version: 0.11
  Description: 
*/

filein "dialogs.ms"

struct b3dObject
(

)

struct chunk
(
  Name = "",
  id = -1,
  Pos = 0
)

struct b3dHeader
(
  
)

struct b3dFile
(
  filename, filestream,
  textureList = #(),
  blockArray = #(),
  header = b3dHeader(),
  fn readHeader =
  (
    -- header size = 24
    fseek 24 
  ), 
  fn readTextureList =
  (
    numTexture = ReadLong filestream #unsigned
    for i = 1 to numTexture do
      append textureList (ReadString filestream)
  ),
  fn readChunkHeader =
  (
    local name = ""
    name = ReadString filestream #unsigned
    if name == undefined then
      fseek 32
    else
      fseek (32 - name.count)    
    result = ReadLong filestream #unsigned
  ),
  fn readChunk =
  (
    local id = readChunkHeader()
    readParammetrs id
  ),  
  fn readChildChunks =
  (
    count = ReadLong filestream #unsigned
    for i = 1 to count do
      readChunk()
  ),  
  fn readParammetrs id =
  (
    case id of
    (
      /*
        id 0 - empty/unused
      */
      0: 
      {
        fseek 44 #seek_cur        
      }; 
      
      /*
        id 1 - empty/unused
      */      
      1: 
      {
        fseek 64 #seek_cur
      }; 
      
      /*
        
      */     
      2: 
      {
        fseek 32
        readChildChunks()
      }; 

      /*
        
      */       
      3: 
        fseek 16
        readChildChunks()
      }; 
      
      4: 
      {
        fseek 80
        readChildChunks()
      }; 
      
      5: 
      {      
        fseek 48
        readChildChunks()
      };
      
      6: 
      {
        fseek (80);
        count = ReadInt(FTell()); 
        fseek (4);
        k = 0;
        while (k < count)  
        {
          fseek (20);
          ++k;
        };      
        readChildChunks()
      };  
    )
  ), 
  fn readChunks =
  (
    fseek filestream 4
    while true do
    (
      readChunk()
    )   
  ),
  fn openFile = 
  (
    filestream = openFileDialog filename
  ),
  fn readFile = 
  (
    readHeader()
    readTextureList()
    readChunks()
  ),
  fn closeFile = 
  (
    close filestream
  ),
  fn init() =
  (
  
  ),
  on create do init()  
)