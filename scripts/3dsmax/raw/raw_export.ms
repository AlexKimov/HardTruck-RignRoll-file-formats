/*
  Author: AlexKimov
  Version: 0.1
  Description: Hard Truck 2 heightmap (.raw) file exporter
  Format: *.raw
  Game: Hard Truck 2 King of the Road 1.3 / Дальнобойщики 2 (8.x)
*/

filein "io/raw.ms"
filein "io/max.ms"

clearlistener()

raw = Heightmapfile()
raw.openFile "wb"
max = Max3ds()
raw.writeFile (max.getSelestedVert(raw.getPointCount())) (max.getSelestedBoundPoint())
raw.closeFile()
	





