import struct
import sys
import timeit
import threading
import pdb


import bmesh
import bpy
import mathutils
import os.path
from bpy.props import *
from bpy_extras.image_utils import load_image
from mathutils import Vector



def uv_from_vert_first(uv_layer, v):
    for l in v.link_loops:
        uv_data = l[uv_layer]
        return uv_data.uv
    return None

def uv_from_vert_average(uv_layer, v):
    uv_average = Vector((0.0, 0.0))
    total = 0.0
    for loop in v.link_loops:
        uv_average += loop[uv_layer].uv
        total += 1.0

    if total != 0.0:
        return uv_average * (1.0 / total)
    else:
        return None

		
def write(file, context, op, filepath):
	
	texNum = 722
	ShapeType = 2 # 2 - normals, 3 - verts+uv(no normal), 258 - rain
	
	
	
	
	verNums = []
	file.write(b'B3D\x00')#struct.pack("4c",b'B',b'3',b'D',b'\x00'))
	ba = bytearray(b'\x00' * 20)
	
	file.write(ba)
	imgs = len(bpy.data.images)
	file.write(struct.pack('<i',imgs))
	imgs = []
	for img in bpy.data.images:
		#img = bpy.data.images[i].name
		imgs.append(img.name)
		file.write(str.encode(img.name))#+ bytearray(b'\x00' * (32-len(img))))
		imgNone = 32-len(img.name)
		ba = bytearray(b'\x00'* imgNone)
		file.write(ba)
	file.write(struct.pack("<i",111))
	
	#print(str(imgs))
	
	
	
	file.write(struct.pack("<i",333))#Null object at the beginning
	file.write(bytearray(b'\x00'*32))
	file.write(bytearray(b'\x00'*16))
	file.write(bytearray(b'\x00'*32))
	file.write(struct.pack("<i",555))
	
	
	objs = len(bpy.data.objects)
	for object in bpy.data.objects:
		verticesL = []
		uvs = []
		faces = []
	
	
	
	
		bm = bmesh.new()
		bm.from_mesh(object.data)
		bm.verts.ensure_lookup_table()
		
		uv_layer = bm.loops.layers.uv[0]
		
		for v in bm.verts:
			uv_first = uv_from_vert_first(uv_layer, v)
			uv_average = uv_from_vert_average(uv_layer, v)
			verticesL.append((v.co,v.normal,uv_average))
		
		
		file.write(struct.pack("<i",333))#{ obj case
		if object.name[0:8] == 'Untitled':
			file.write(bytearray(b'\x00'*32))
		else:
			file.write(str.encode(object.name)+bytearray(b'\x00'*(32-len(object.name))))
		#print (str(int(object['1 type'])))
		
		meshdata = object.data
		
		# for vert in object.data.vertices:
			# verticesL.append(((vert.co.x,vert.co.y,vert.co.z),(vert.normal[0],vert.normal[1],vert.normal[2])))
		
		
		#print (str(verticesL))
		
		
		
		
		for i, polygon in enumerate(meshdata.polygons):
			#print('polygon: ', i)
			for i1, loopindex in enumerate(polygon.loop_indices):
				#print('meshloop: ', i1, ' index: ',loopindex)
				meshloop = meshdata.loops[loopindex]
				faces.append(meshloop.vertex_index)
				uvs.append(meshdata.uv_layers[0].data[loopindex].uv)
			verNums.extend(polygon.vertices)
			
			
			
			
			
		#print(str(len(meshdata.uv_layers[0].data)))
		#print(str(faces))
		
		file.write(struct.pack("<i",int(37)))
		
		file.write(bytearray(b'\x00'*16))
		file.write(bytearray(b'\x00'*32))
		vLen = len(verticesL)

		file.write(struct.pack("<i",ShapeType))
		file.write(struct.pack("<i",vLen))

		for i,vert in enumerate(verticesL):
			file.write(struct.pack("<f",vert[0][0]))
			file.write(struct.pack("<f",vert[0][1]))
			file.write(struct.pack("<f",vert[0][2]))
			
			# uvInd = verNums.index(i)
			
			# file.write(struct.pack("<f",object.data.uv_layers[0].data[uvInd].uv.x))
			# file.write(struct.pack("<f",1-object.data.uv_layers[0].data[uvInd].uv.y))
			

			file.write(struct.pack("<f",vert[2][0]))

			file.write(struct.pack("<f",1-vert[2][1]))
			file.write(struct.pack("<f",vert[1][0]))
			file.write(struct.pack("<f",vert[1][1]))
			file.write(struct.pack("<f",vert[1][2]))
			if ((ShapeType == 258) or (ShapeType == 515)):
				file.write(struct.pack("<2f",0,1))
			elif (ShapeType == 514):
				file.write(struct.pack("<4f",0,1,0,1))
			
		file.write(struct.pack("<i",1))
		
		file.write(struct.pack("<i",333))
		if object.name[0:8] == 'Untitled':
			file.write(bytearray(b'\x00'*32))
		else:
			file.write(str.encode(object.name)+bytearray(b'\x00'*(32-len(object.name))))

			
		file.write(struct.pack("<i",int(35)))
		
		file.write(bytearray(b'\x00'*16))
		fLen = len(object.data.loops)//3
		file.write(struct.pack("<i",3))
		file.write(struct.pack("<i",texNum))
		file.write(struct.pack("<i",fLen))
		#print (faces)
		for i in range(fLen):
			file.write(struct.pack("<i",16))
			file.write(struct.pack("<f",1.0))
			file.write(struct.pack("<i",32767))
			file.write(struct.pack("<i",texNum))
			file.write(struct.pack("<i",3))#VerNum
			file.write(struct.pack("<3i",faces[i*3],faces[i*3+1],faces[i*3+2]))
			#file.write(struct.pack("<iffiffiff",faces[i*3],verticesL[faces[i*3]][2][0],1-verticesL[faces[i*3]][2][1],faces[i*3+1],verticesL[faces[i*3+1]][2][0],1-verticesL[faces[i*3+1]][2][1],faces[i*3+2],verticesL[faces[i*3+2]][2][0],1-verticesL[faces[i*3+2]][2][1]))
			verticesL

		file.write(struct.pack("<i",555))
		file.write(struct.pack("<i",555))
	file.write(struct.pack("<i",222))#EOF
		
		
