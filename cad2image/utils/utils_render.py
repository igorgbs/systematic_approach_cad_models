import bpy
import numpy as np
import sys

# sys.path.append("/home/jorisguerin/Code/cad2image/params/")
sys.path.append("../params/")
from params_render import *

def random_cam_pose():

    dist = np.random.randint(distance_range_cam[0], distance_range_cam[1])
    rot = [np.random.randint(rotation_range_cam[i][0],
           rotation_range_cam[i][1]) for i in range(2)]

    x = dist * np.sin(np.deg2rad(rot[0])) * np.sin(np.deg2rad(rot[1]))
    y = - dist * np.sin(np.deg2rad(rot[0])) * np.cos(np.deg2rad(rot[1]))
    z = dist * np.cos(np.deg2rad(rot[0]))

    location = [x, y, z]
    rotation = [np.deg2rad(rot[0]), 0, np.deg2rad(rot[1])]

    return [location, rotation]

def add_cam(location = "random", rotation = "random"):

    cam_data = bpy.data.cameras.new(name="Camera")
    cam_object = bpy.data.objects.new(name="Camera", object_data = cam_data)
    bpy.context.scene.objects.link(cam_object)
    bpy.context.scene.camera = cam_object

    cam_object.data.clip_end = clip_end

    if location == "random" or rotation == "random":
        locrot = random_cam_pose()
        location = locrot[0]
        rotation = locrot[1]

    cam_object.location = location
    cam_object.rotation_euler = rotation

def check_gpu_exists():
    all_gpu_names = [bpy.context.user_preferences.addons['cycles'].preferences.devices[i].name for i in range(len(bpy.context.user_preferences.addons['cycles'].preferences.devices))]
    if gpu_name not in all_gpu_names:
        print("Error: %s is not among the available CUDA devices." % gpu_name)
        print("Please change 'gpu_name' in render_params to one of the following:\n")
        for i in range(len(bpy.context.user_preferences.addons['cycles'].preferences.devices)):
            print(bpy.context.user_preferences.addons['cycles'].preferences.devices[i].name)
        return False
    return True

def render(destination = "./render.png", contrast = "Base Contrast", resolution = 1.0):
# Accepted contrasts: "Very Low Contrast", "Low Contrast", "Medium Low Contrast", "Base Contrast", "High Contrast", "Very High Contrast"

    if type(resolution) == float:
        resolution = [resolution * 1920, resolution * 1080]

    bpy.context.scene.view_settings.view_transform = 'Filmic'
    bpy.context.scene.view_settings.look = 'Filmic - Base Contrast'

    bpy.context.scene.render.filepath = destination
    bpy.context.scene.render.resolution_x = resolution[0]
    bpy.context.scene.render.resolution_y = resolution[1]
    bpy.data.scenes["Scene"].render.resolution_percentage = 100
    bpy.context.scene.cycles.samples = 120

    if rendering_type == "cpu":
        bpy.context.scene.cycles.device = "CPU"
        bpy.context.scene.render.tile_x = 16
        bpy.context.scene.render.tile_y = 16
    elif rendering_type == "gpu":
        isGpu = check_gpu_exists()
        if not isGpu:
            return -1
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = "NONE"
        for i in range(len(bpy.context.user_preferences.addons['cycles'].preferences.devices)):
            bpy.context.user_preferences.addons['cycles'].preferences.devices[i]['use'] = False
        bpy.context.user_preferences.addons['cycles'].preferences.devices[gpu_name]["use"] = True
        bpy.context.scene.cycles.device = "GPU"
        bpy.context.scene.render.tile_x = 256
        bpy.context.scene.render.tile_y = 256
    else:
        print("Error, rendering type should be either 'cpu' or 'gpu'. Please change this in the params_render file")
    bpy.ops.render.render(write_still = True)
