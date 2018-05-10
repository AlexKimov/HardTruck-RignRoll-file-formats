import struct
import sys
import timeit
import threading
import pdb

import bpy
import mathutils
import os.path
from bpy.props import *
from bpy_extras.image_utils import load_image

def openclose(file):
	oc = file.read(4)	
	if (oc == (b'\x4D\x01\x00\x00')):
		return 2
	elif oc == (b'\x2B\x02\x00\x00'):
		# print('}')
		return 0
	elif oc == (b'\xbc\x01\x00\x00'):
		#print('BC01')
		return 3
	elif oc == (b'\xde\x00\00\00'):
		print ('EOF')
		return 1
	else:
		print(str(file.tell()))
		print (str(oc))
		print('brackets error')
		sys.exit()

def onebyte(file):
	return (file.read(1))
	
	
		
class type05:
	name_fmt = '32c'
	byte1 = 'c'
	byte3 = '3c'
	def __init__(self,file):
		self.name = file.read(struct.calcsize(self.name_fmt)).decode("utf-8")
		_s = file.read(struct.calcsize(self.byte1))
		self.byte1 = struct.unpack(self.byte1,_s)
		_s = file.read(struct.calcsize(self.byte3))
		self.byte3 = struct.unpack(self.byte3,_s)
		
class type15:
	byte1 = 'c'
	byte1_2 = 'c'
	byte4 = '4c'
	byte3 = '3c'
	def __init__(self,file):
		self.byte1 = onebyte(file)					
		file.seek(3,1)								#
		
		_s = file.read(struct.calcsize(self.byte4))	#
		self.byte4 = struct.unpack(self.byte4,_s)
		
		self.byte1_2 = onebyte(file)				# кол-во вложеных обьектов 25
		
		_s = file.read(struct.calcsize(self.byte3))
		self.byte3 = struct.unpack(self.byte3,_s)
				

class coords3:
	def __init__(self, file):
		self.v = struct.unpack("<3f", file.read(12))

class quat:
	fmt = 'ffff'

	def __init__(self, file):
		_s = file.read(struct.calcsize(self.fmt))
		self.v = struct.unpack(self.fmt, _s)
		# Quats are stored x,y,z,w - this fixes it
		self.v = [self.v[-1], self.v[0], self.v[1], self.v[2]]
		
		
def read(file, context, op, filepath):
	if file.read(3) == b'b3d':
		print ("correct file");
	else:
		print ("b3d error")
		
	file.seek(21,1);
	Imgs = []
	math = []
	#texr = []
	for i in range(struct.unpack('<i',file.read(4))[0]):
		#Imgs.append(file.read(32).decode("utf-8").rstrip('\0'))
		
		SNImg = file.read(32).decode("utf-8").rstrip('\0') #читаю имя
		PImg = (filepath.rsplit('\\',1)[0] +'\\txr\\' +SNImg+'.tga') #полный путь
		#print (PImg)
		if os.path.isfile(PImg):
			img = bpy.data.images.load(PImg)
		else:
			PImg = (filepath.rsplit('\\',1)[0] +'\\txr\\' +SNImg[4:]+'.tga') #полный путь
			if os.path.isfile(PImg):
				img = bpy.data.images.load(PImg)
			else:
				img = bpy.data.images.new(SNImg,1,1)
				print ('no '+PImg+' image')
		Imgs.append(img)
		
		
		tex = bpy.data.textures.new(SNImg,'IMAGE') 
		tex.use_preview_alpha = True
		tex.image = img #bpy.data.images[i]
		mat = bpy.data.materials.new(SNImg)
		mat.texture_slots.add()
		mat.texture_slots[0].uv_layer = 'UVmap'
		mat.texture_slots[0].texture = tex
		mat.texture_slots[0].use_map_alpha = True
		math.append(mat)
		
		
	file.seek(4,1)		
	
	ex = 0
	i = 0
	lvl = 0
	cnt = 0
	coords25 = []
	coords23 = []
	vertexes = []
	#
	b3dObj = 0
	uv = []
	b3dObj = bpy.data.objects.new(os.path.basename(op.properties.filepath),None)
	context.scene.objects.link(b3dObj)
	
	objString = [os.path.basename(op.properties.filepath)]
	while ex!=1:


		#if (file.tell()>23281193):
		#	break
		
		ex = openclose(file)
		if ex == 0:
			#print('-')
			objString = objString[:-1]
			lvl-=1
			#print((objString))
			#print('eob')
			#continue
		elif ex == 1: 
			print(str(cnt))
			file.close()
			break

		elif ex == 3:
			continue
		elif ex == 2:
			#print ('+')
			lvl+=1
			objName = file.read(32).decode("cp1251").rstrip('\0')
			type = 	struct.unpack("<i",file.read(4))[0]
			#print (str(type))
			if (type == 0):
				qu = quat(file).v
				objString.append(os.path.basename(op.properties.filepath))
				ff = file.seek(28,1)
			
			elif (type == 1):
				cnt+=1
				#b3dObj.append(
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '1'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				b3dObj['2 name'] = file.read(32).decode("cp1251").rstrip('\0')
				b3dObj['3 name'] = file.read(32).decode("cp1251").rstrip('\0')

			elif (type == 2):	#контейнер хз
				cnt+=1
				#b3dObj.append(
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '2'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				
				qu = quat(file).v
				struct.unpack("<4fi",file.read(20))
			elif (type == 3):	#
				cnt+=1
				#b3dObj.append(
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '3'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				
				qu = quat(file).v
				struct.unpack("<i",file.read(4))
			elif (type == 4):	#похоже на контейнер 05 совмещенный с 12
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '4'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				
				qu = quat(file).v
				str(file.read(32).decode("utf-8")).rstrip('\0')
				struct.unpack("<i7fi",file.read(36))
				
				
			elif (type==5): #общий контейнер
				qu = quat(file).v
				
				object = type05(file)
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '5'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
			elif (type == 6):	
				vertexes = []
				uv = []

				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '6'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				
				qu = quat(file).v
				str(file.read(32).decode("utf-8")).rstrip('\0')
				str(file.read(32).decode("utf-8")).rstrip('\0')
				num = struct.unpack("<i",file.read(4))[0]
				for i in range (num):
					vertexes.append(struct.unpack("<3f",file.read(12)))
					uv.append(struct.unpack("<2f",file.read(8)))
				struct.unpack("<i",file.read(4))[0]
			elif (type == 7):	#25? xyzuv TailLight? похоже на "хвост" движения	mesh
				coords25 = []
				vertexes = []
				uv = []
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '7'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				

					
				qu = quat(file).v
				str(struct.unpack("<8f",file.read(32))) #0-0
				
				
				num = struct.unpack("<i",file.read(4))[0]
				for i in range(num):
					vertexes.append(struct.unpack("<3f",file.read(12)))
					uv.append(struct.unpack("<2f",file.read(8)))
					#str(struct.unpack("<5f",file.read(20)))
				str(struct.unpack("<i",file.read(4))[0])
				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				
			elif (type == 8):	#тоже фейсы		face
				faces = []
				faces_all = []
				uvs = []
				texnum = 0
				cnt+=1
				b3dMesh = (bpy.data.meshes.new(objName))
				b3dObj=bpy.data.objects.new(objName, b3dMesh)
				b3dObj['1 type'] = '8'
				b3dObj.parent = context.scene.objects[objString[-1]]
				
				b3dObj.hide = True	


				qu = quat(file).v
				num = struct.unpack("<i",file.read(4))[0]
				for i in range(num):
					faces = []
					faces_new = []
					format = struct.unpack("<i",file.read(4))[0]
					
					struct.unpack("<fi",file.read(8))
					texnum = struct.unpack("i",file.read(4))[0]
					
					num1 = struct.unpack("<i",file.read(4))[0]
					
					if ((format == 178) or (format == 50)):
						for j in range(num1):
							faces.append(struct.unpack("<i",file.read(4))[0])							
							struct.unpack("<5f",file.read(20))
					elif ((format == 176) or (format == 48)or (format == 179)or (format == 51)):
						for j in range(num1):
							faces.append(struct.unpack("<i",file.read(4))[0])							
							struct.unpack("<3f",file.read(12))
					elif ((format == 3) or (format == 2) or (format == 131)):
						for j in range(num1):
							faces.append(struct.unpack("<i",file.read(4))[0])							
							struct.unpack("<2f",file.read(8))
					elif format == 177:
						for j in range(num1):
							faces.append(struct.unpack("<i",file.read(4))[0])							
							struct.unpack("<f",file.read(4))
					else:
						for j in range(num1):
							faces.append(struct.unpack("<i",file.read(4))[0])
						#print ('faces:	'+str(faces))
					for t in range(len(faces)-2):
						if t%2 ==0:
							faces_new.append([faces[t],faces[t+1],faces[t+2]])
						else:
							if ((format == 0) or (format == 16) or (format == 1)):
								faces_new.append([faces[t+2],faces[t+1],faces[0]])
							else:
								faces_new.append([faces[t+2],faces[t+1],faces[t]])
						uvs.append((uv[faces_new[t][0]],uv[faces_new[t][1]],uv[faces_new[t][2]]))
					faces_all.extend(faces_new)
					#print(str(faces_all))
				#pdb.set_trace()
				Ev = threading.Event()
				Tr = threading.Thread(target=b3dMesh.from_pydata, args = (vertexes,[],faces_all))
				Tr.start()
				Ev.set()
				Tr.join()

				
				uvMesh = b3dMesh.uv_textures.new()
				imgMesh = math[texnum].texture_slots[0].texture.image.size[0]
				uvMesh.name = 'default'
				uvLoop = b3dMesh.uv_layers[0]
				uvsMesh = []
				
				#print('uvs:	',str(uvs))
				for i, texpoly in enumerate(uvMesh.data):
					texpoly.image = Imgs[texnum]
					poly = b3dMesh.polygons[i]
					for j,k in enumerate(poly.loop_indices):
						uvsMesh = [uvs[i][j][0],1 - uvs[i][j][1]]
						uvLoop.data[k].uv = uvsMesh
						
				mat = b3dMesh.materials.append(math[texnum])

				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
							
			elif (type == 9):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '9'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				

				qu = quat(file).v
				str(quat(file).v)
				#print
				file.seek(4,1)
			elif (type == 10): #контейнер, хз о чем
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '10'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				
				qu = quat(file).v
				quat(file)
				(onebyte(file))
				file.seek(3,1)
			elif (type == 12):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '12'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				qu = quat(file).v
				file.read(28)
	
			elif (type == 13):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '13'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

			
				qu = quat(file).v
				num = []
				coords = []
				num = struct.unpack("3i",file.read(12))
				#printwrite(writefile,tab1+str(num))
				for i in range(num[-1]):
					coords.append(struct.unpack("f",file.read(4))[0])
				if num[-1]>0:
					pass
					#printwrite(writefile,tab1+'0d Coords:	'+str(coords))
					
			elif (type == 14): #sell_ ? 
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '14'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				qu = quat(file).v
				file.seek(17,1)
				file.seek(11,1)#0-0
				
			elif (type == 16):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '16'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				qu = quat(file).v
				struct.unpack("11f",file.read(44))
			elif (type == 17):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '17'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				qu = quat(file).v
				struct.unpack("11f",file.read(44))
				
			elif (type == 18):	#контейнер "применить к"
				qu = quat(file).v
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '18'
				b3dObj['2 attr of'] = file.read(32).decode("utf-8").rstrip('\0')
				b3dObj['3 attr to'] = file.read(32).decode("utf-8").rstrip('\0')
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				
			elif (type == 19):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '19'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
			
				num = []
				num.append(struct.unpack("i",file.read(4))[0])
				#printwrite(writefile,tab1+str(num))

	
			elif (type == 20):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '20'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)

				qu = quat(file).v
			
				title = []
				title = struct.unpack("4i",file.read(16))
				coords = []
				coords1 = []
				#printwrite(writefile,tab1+str(title))
				for i in range (title[0]):
					coords = struct.unpack("fff",file.read(12))
					#printwrite(writefile,tab1+str(coords))
				for i in range (title[3]):
					coords1.append(struct.unpack("f",file.read(4))[0])
				#printwrite(writefile,tab1+str(coords1))

			
			
			elif (type == 21): #testkey??? 
				qu = quat(file).v
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '21'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
				object = type15(file)
				


			elif (type == 23): #colision mesh
				
				cnt+=1
				b3dMesh = (bpy.data.meshes.new(objName))
				b3dObj = bpy.data.objects.new(objName, b3dMesh)
				b3dObj['1 type'] = '23'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				
				
				#qu = quat(file).v

				x = struct.unpack("<i",file.read(4))[0]
				y = struct.unpack("<i",file.read(4))[0]
				z = struct.unpack("<i",file.read(4))[0]
				for i in range(z):
					struct.unpack("<i",file.read(4))[0]

				num = struct.unpack("<i",file.read(4))[0]
				for i in range(num):
					num1 = struct.unpack("<i",file.read(4))[0]
					for j in range(num1):
						coords3(file).v

				
				
				
				# mesh = []
				# meshFaces = []
				# numCnt = 0
				
				# num = struct.unpack("<i",file.read(4))[0]
				# #print (str(num))
				# for i in range(num):
					# num1 = struct.unpack("<i",file.read(4))[0]
					# #print ('num1:	'+str(num1))
					# numCnt = numCnt + num1
					# #mesh = []
					# faces = []
					# for j in range(num1):
						# #print(str(file.tell()))
						# mesh.append(coords3(file).v)
						# faces.append(j)
					# meshFaces.append(faces)
				
			elif (type == 24): #настройки положения обьекта
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '24'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				
				qu = quat(file).v
				objString.append(context.scene.objects[0].name)
				file.seek(20,1)
				struct.unpack("<fff",file.read(12))
				file.seek(8,1)#01 00 00 00
				
			elif (type == 25): #copSiren????/ контейнер
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '25'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
			
				qu = coords3(file).v
				file.seek(32,1)
				ff = file.read(4)
				for i in range(10):
					file.seek(4,1)
			elif (type == 28): #face
				
				cnt+=1
				b3dMesh = (bpy.data.meshes.new(objName))
				#print('cnt:	'+str(cnt))
				b3dObj = bpy.data.objects.new(objName, b3dMesh)
				b3dObj['1 type'] = '28'
				
				b3dObj.parent = context.scene.objects[objString[-1]]
				
				b3dObj.hide = True				
				coords = []
				
				qu = quat(file).v
				file.seek(12,1)
				
				num = struct.unpack("<i",file.read(4))[0]
				#print(str(coords))
				if num == 1:
					coords.extend(struct.unpack("if3i",file.read(20)))
					if (coords[0]>1):
						for i in range(coords[4]):
							coords.extend(struct.unpack("<4f",file.read(16)))
					else:
						coords.extend(struct.unpack("<8f",file.read(32)))

				elif num ==2:
					coords.extend(struct.unpack("if3i",file.read(20)))
					for i in range(num*2):
						coords.extend(struct.unpack("<7f",file.read(28)))
					coords.extend(struct.unpack("<f",file.read(4)))
					
				elif ((num == 10) or(num == 6)) : #db1
					for i in range(num):
						coords.extend(struct.unpack("if3i",file.read(20)))	
						num1 = coords[-1]
						for i in range (num1):
							coords.append(struct.unpack("<2f",file.read(8)))
				#b3dMesh.from_pydata(vertexes,[],faces)
				
				context.scene.objects.link(b3dObj) #добавляем в сцену обьект
				objString.append(context.scene.objects[0].name)
				
			elif (type == 29):	
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '29'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				
				qu = quat(file).v
				num0 = struct.unpack("<i",file.read(4))[0]
				struct.unpack("<i",file.read(4))[0]
				struct.unpack("<7f",file.read(28))
				if num0 == 4:
					struct.unpack("<f",file.read(4))[0]
				elif num0 == 3:
					pass
				struct.unpack("<i",file.read(4))[0]
			elif (type == 30):	
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '30'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)

				qu = quat(file).v
				file.read(32)
				
				file.read(24)
			elif (type == 31):	
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '31'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)

				qu = quat(file).v
				struct.unpack("<i4f",file.read(20))
				struct.unpack("<i4f",file.read(20))
				for i in range(27):
					struct.unpack("<if",file.read(8))
				struct.unpack("<i",file.read(4))
			elif (type == 33): #lamp
				
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '33'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				qu = quat(file).v
				ff = file.read(4)
				for i in range(18):
					file.seek(4,1)
					
			elif (type == 34): #lamp
				num = 0
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '34'
				b3dObj.parent = context.scene.objects[objString[-1]]
				b3dObj.hide = True				
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				
				qu = quat(file).v
				ff = file.read(4)
				num = struct.unpack("<i",file.read(4))[0]
				for i in range(num):
					file.seek(16,1)
			elif (type == 35): #mesh
				coords23 = []
				
				cnt+=1
				b3dMesh = (bpy.data.meshes.new(objName))
				#print('cnt:	'+str(cnt))
				b3dObj = bpy.data.objects.new(objName, b3dMesh)
				b3dObj['1 type'] = '35'
				
				b3dObj.parent = context.scene.objects[objString[-1]]
				
				b3dObj.hide = True				
				qu = quat(file).v
				faces = []
				num0 = struct.unpack("<i",file.read(4))[0]
				file.seek(4,1)
				num = struct.unpack("<i",file.read(4))[0]
				uvs = []
				########

				########
				faces1 = []
				
				#print (str(file.tell()))
				if num0<3:
					for i in range(num):
						faces1 = []
						num1=[]
						#coords23.append(struct.unpack("<i",file.read(4)))
						num1.append(struct.unpack("<i",file.read(4))[0])
						#print(str(file.tell()))
						if (num1[0] == 50):
							num1.extend(struct.unpack("<f4i5fi5fi5f",file.read(88)))
							coords23.append(num1)
							faces1 = (coords23[i][5],coords23[i][11],coords23[i][17])

						elif (num1[0] == 49):
							num1.extend(struct.unpack("<f3iififif",file.read(40)))
							coords23.append(num1)
							#print ('co23:	'+str(coords23))
							faces1 = (coords23[i][5],coords23[i][7],coords23[i][9])
						elif((num1[0] == 1) or (num1[0] == 0)):

							num1.extend(struct.unpack("<f6i",file.read(28)))
							coords23.append(num1)
							faces1 = coords23[i][5:8]
							#print('num1:	'+str(num1))
							# faces1 = coords23[i][4:7]
							# faces.append(faces1)
						elif ((num1[0] == 2) or (num1[0] == 3)):
							num1.extend(struct.unpack("<fiiiiffiffiff",file.read(52)))	
							coords23.append(num1)
							faces1=(coords23[i][5],coords23[i][8],coords23[i][11])
						else:
							num1.extend(struct.unpack("<f3iifffifffifff",file.read(64)))
							coords23.append(num1)
							faces1 = (coords23[i][5],coords23[i][9],coords23[i][13])
						#faces1 = faces1[0]
						faces.append(faces1)
						#faces1 = faces1[0]
						#uvs.append((coords25[faces1[0]][3:5] , coords25[faces1[1]][3:5] , coords25[faces1[2]][3:5]))
						#print ('faces	' + str(faces1)+'	'+str(uv))
						#print('f0:	'+str(faces1))
						#print(str(num1))
						#print(str(file.tell()))
						uvs.append((uv[faces1[0]],uv[faces1[1]],uv[faces1[2]]))
						
				elif num0 == 3:
					#print(str(num))
					for i in range(num):
						#coords23.append([struct.unpack("<i",file.read(4))[0]])
						#file.read(4)
						#print(str(num)+'	'+str(i))
						coords23.append(struct.unpack("<if6i",file.read(32)))
						faces1 = coords23[i][5:8]
						faces.append(faces1)
						uvs.append((uv[faces1[0]],uv[faces1[1]],uv[faces1[2]]))
						#print (str(coords23))
						#print ('faces	' + str(faces1)+'	'+str(uv))
						
				Ev = threading.Event()
				Tr = threading.Thread(target=b3dMesh.from_pydata, args = (vertexes,[],faces))
				Tr.start()
				Ev.set()
				Tr.join()
				
				#b3dMesh.from_pydata(vertexes,[],faces)
				
				#print ('25:		' + str(coords23))
						
				uvMesh = b3dMesh.uv_textures.new()
				#b3dMesh.use_mirror_topology = True
				#imgMesh = math[coords23[i][3]].texture_slots[0].texture.image.size[0]
				uvMesh.name = 'UVmap'
				uvLoop = b3dMesh.uv_layers[0]
				uvsMesh = []
				#print('uvs:	'+str(uvs))
				
				#uvMain = createTextureLayer("default", b3dMesh, uvs)
				
				for i, texpoly in enumerate(uvMesh.data):
					poly = b3dMesh.polygons[i]
					texpoly.image = Imgs[coords23[i][3]]
					for j,k in enumerate(poly.loop_indices):
						uvsMesh = [uvs[i][j][0],1 - uvs[i][j][1]]
						uvLoop.data[k].uv = uvsMesh
						
				
				b3dMesh.materials.append(math[coords23[i][3]])
				
				
				b3dMesh.uv_textures['UVmap'].active = True
				b3dMesh.uv_textures['UVmap'].active_render = True



				context.scene.objects.link(b3dObj) #добавляем в сцену обьект
				objString.append(context.scene.objects[0].name)

			elif (type == 36):
				qu = quat(file).v
				coords25 = []
				vertexes = []
				uv = []
				b3dObj['2 name'] = file.read(32).decode("cp1251").rstrip('\0')
				b3dObj['3 name'] = file.read(32).decode("cp1251").rstrip('\0')
				num = struct.unpack("<i",file.read(4))[0]
				iter = struct.unpack("<i",file.read(4))[0]
				if num == 0:
					objString.append(objString[-1])
					pass
				else:
					cnt+=1
					b3dObj = bpy.data.objects.new(objName, None)
					b3dObj['1 type'] = '36'
					b3dObj.parent = context.scene.objects[objString[-1]]
					context.scene.objects.link(b3dObj)
					objString.append(context.scene.objects[0].name)
					b3dObj.hide = True				
					if num == 2:
						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(12,1)
					elif num ==3:

						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(4,1)
							
					elif ((num ==258) or (num ==515)):

						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(20,1)
					elif num ==514:
						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							struct.unpack("<7f",file.read(28))
					#print(str(objName))
							
				file.seek(4,1)#01 00 00 00 subblocks count

			elif (type == 37):
				qu = quat(file).v
				coords25 = []
				vertexes = []
				uv = []
				file.seek(32,1)
				num = struct.unpack("<i",file.read(4))[0]
				iter = struct.unpack("<i",file.read(4))[0]
				if num == 0:
					objString.append(objString[-1])
					pass
				else:
					cnt+=1
					b3dObj = bpy.data.objects.new(objName, None)
					b3dObj['1 type'] = '37'
					b3dObj.parent = context.scene.objects[objString[-1]]
					context.scene.objects.link(b3dObj)
					objString.append(context.scene.objects[0].name)
					b3dObj.hide = True				
					if num == 2:
						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(12,1)
					elif num ==3:

						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(4,1)
							
					elif ((num ==258) or (num ==515)):

						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							file.seek(20,1)
					elif num ==514:
						for i in range(iter):
							vertexes.append(struct.unpack("<3f",file.read(12)))
							uv.append(struct.unpack("<2f",file.read(8)))
							struct.unpack("<7f",file.read(28))
					#print(str(objName))
							
				file.seek(4,1)#01 00 00 00 subblocks count
			elif (type == 39):
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '39'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				
			
				qu = quat(file).v
				quat(file)
				file.read(4)
				
				struct.unpack("<i",file.read(4))

			elif (type == 40):
				data = []
				data1 = []
				cnt+=1
				b3dObj = bpy.data.objects.new(objName, None)
				b3dObj['1 type'] = '40'
				b3dObj.parent = context.scene.objects[objString[-1]]
				context.scene.objects.link(b3dObj)
				objString.append(context.scene.objects[0].name)
				b3dObj.hide = True				

				qu = quat(file).v
				file.read(32)
				file.read(32)
				#file.read(52)
				data = struct.unpack("<3i",file.read(12))
				for i in range (data[-1]):
					data1.append(struct.unpack("f", file.read(4))[0])
				#print (str(data[-1])+'	'+str(data1))
			
			else:
				print(str(file.tell()))
				print ('smthng wrng')
				return
			#print(objName)
			
