import bpy
import numpy as np
import sys

from params_light import *

def add_sunLight(strength = "random", rotation = "random"):
# Sun lamps are independant of location

    lamp_data = bpy.data.lamps.new(name = "Sun", type = "SUN")
    lamp_data.use_nodes = True

    if strength == "random":
        strength = np.max([0.5,np.random.normal(stgth_stats_sun[0], stgth_stats_sun[1])])
    lamp_data.node_tree.nodes['Emission'].inputs['Strength'].default_value = strength

    lamp_object = bpy.data.objects.new(name = "Sun", object_data = lamp_data)
    bpy.context.scene.objects.link(lamp_object)

    if rotation == "random":
        rotation = [np.random.randint(np.deg2rad(rot_range_sun[i][0]),
                    np.deg2rad(rot_range_sun[i][1])) for i in range(3)]
    lamp_object.rotation_euler = rotation

def add_pointLight(strength = "random", location = "random"):
# Point lamps are independant of rotation

    lamp_data = bpy.data.lamps.new(name = "Point", type = "POINT")
    lamp_data.use_nodes = True

    if strength == "random":
        strength = np.max([0.0, np.random.normal(stgth_stats_point[0], stgth_stats_point[1])])
    lamp_data.node_tree.nodes['Emission'].inputs['Strength'].default_value = strength

    lamp_object = bpy.data.objects.new(name = "Point", object_data = lamp_data)
    bpy.context.scene.objects.link(lamp_object)

    if location == "random":
        location = [np.random.randint(loc_range_point[i][0],
                    loc_range_point[i][1]) for i in range(3)]
    lamp_object.location = location

def add_spotLight(strength = "random", dimension = "random", location = "random",
                  rotation = "random"):

    lamp_data = bpy.data.lamps.new(name = "Spot", type = "SPOT")
    lamp_data.use_nodes = True

    if strength == "random":
        strength = np.max([0.0, np.random.normal(stgth_stats_point[0], stgth_stats_point[1])])
    lamp_data.node_tree.nodes['Emission'].inputs['Strength'].default_value = strength

    if dimension == "random":
        dimension = np.random.randint(dim_range_spot[0], dim_range_spot[1])
    lamp_data.spot_size = np.deg2rad(dimension)

    lamp_object = bpy.data.objects.new(name = "Spot", object_data = lamp_data)
    bpy.context.scene.objects.link(lamp_object)

    if location == "random" or rotation == "random":
        intersect_pt = [np.random.randint(intersection_range_spot[i][0],
                       intersection_range_spot[i][1]) for i in range(2)]
        dist = np.random.randint(distance_range_spot[0], distance_range_spot[1])
        rot = [np.random.randint(rot_range_spot[i][0],
               rot_range_spot[i][1]) for i in range(2)]

        x = intersect_pt[0] + dist * np.sin(np.deg2rad(rot[0])) * np.sin(np.deg2rad(rot[1]))
        y = intersect_pt[1] - dist * np.sin(np.deg2rad(rot[0])) * np.cos(np.deg2rad(rot[1]))
        z = dist * np.cos(np.deg2rad(rot[0]))

        location = [x, y, z]
        rotation = [np.deg2rad(rot[0]), 0, np.deg2rad(rot[1])]

    lamp_object.location = location
    lamp_object.rotation_euler = rotation

def add_lamp(ltype = "SUN", strength = "random", location = "random", rotation = "random"):
# Add a light source to the scene.
# Type can be "SUN", "POINT", "AREA" or "SPOT"

    lamp_data = bpy.data.lamps.new(name = "Lamp", type = ltype)
    lamp_data.use_nodes = True
    if strength != "random":
        lamp_data.node_tree.nodes['Emission'].inputs['Strength'].default_value = strength
    else:
        if ltype == "SUN":
            lamp_data.node_tree.nodes['Emission'].inputs['Strength'].default_value = np.random.normal(stgth_stats_sun[0], stgth_stats_sun[1])

    lamp_object = bpy.data.objects.new(name="Lamp", object_data = lamp_data)
    bpy.context.scene.objects.link(lamp_object)

    if rotation != "random":
        lamp_object.rotation_euler = rotation
    else:
        if ltype == "SUN":
            lamp_object.rotation_euler = [np.random.randint(np.deg2rad(rot_range_sun[i][0]),
                                         np.deg2rad(rot_range_sun[i][1])) for i in range(3)]
        if ltype == "POINT":
            pass # rotation for POINT is not important
        if ltype == "AREA":
            lamp_object.location = [np.random.randint(np.deg2rad(rot_range_area[i][0]),
                                    np.deg2rad(rot_range_area[i][1])) for i in range(3)]
        if ltype == "SPOT":
            lamp_object.location = [np.random.randint(np.deg2rad(rot_range_spot[i][0]),
                                    np.deg2rad(rot_range_spot[i][1])) for i in range(3)]

    if location != "random":
        lamp_object.location = location
    else:
        if ltype == "SUN":
            pass # Location for SUN is not important
        if ltype == "POINT":
            lamp_object.location = [np.random.randint(loc_range_point[i][0], loc_range_point[i][1]) for i in range(3)]
        if ltype == "AREA":
            lamp_object.location = [np.random.randint(loc_range_area[i][0], loc_range_area[i][1]) for i in range(3)]
        if ltype == "SPOT":
            lamp_object.location = [np.random.randint(loc_range_spot[i][0], loc_range_spot[i][1]) for i in range(3)]
