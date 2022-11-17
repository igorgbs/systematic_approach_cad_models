import bpy
import numpy as np

#from utils_material import *

def clear_scene(delCam = 1, delLamp = 1):
# Empty the scene of all objects and meshes
# Set delCam and delLamp to 0 if you want to keep
# The initial lamp and cam

    for obj in bpy.data.objects:
        if obj.name != "Camera" and obj.name != "Lamp":
            bpy.data.objects.remove(obj)
        elif delCam == 1 and obj.name == "Camera":
            bpy.data.objects.remove(obj)
        elif delLamp == 1 and obj.name == "Lamp":
            bpy.data.objects.remove(obj)
    for gp in bpy.data.groups:
    	if gp != "RigidBodyWorld":
    		bpy.data.groups.remove(gp)

    for msh in bpy.data.meshes:
        bpy.data.meshes.remove(msh)

    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)

def import_mesh(mesh_path, object_name, initial_location = [0,0,0],
				initial_rotation = [0,0,0],	texture_path = None):

    bpy.ops.import_mesh.stl(filepath = mesh_path)

    activeObject = bpy.context.selected_objects[0]
    activeObject.name = object_name

    bpy.ops.object.origin_set(type = "ORIGIN_CENTER_OF_MASS")
    activeObject.location = initial_location
    activeObject.rotation_euler = initial_rotation

    # if texture_path != None:
    # 	mat_name = texture_path.split("/")[-2]
    # 	if mat_name in [bpy.data.materials[i].name for i in range(len(bpy.data.materials))]:
    # 		activeObject.data.materials.append(bpy.data.materials[mat_name])
    # 	else:
    #     	set_material(activeObject, mat_name, texture_path)

def select_objects(list_of_objects):
    for obj in bpy.data.objects:
        if obj.name in list_of_objects:
            bpy.data.objects[obj.name].select = True
        else:
            obj.select = False
