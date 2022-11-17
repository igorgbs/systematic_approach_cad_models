import bpy

from utils_scene import *

def activate_physics(object_name, mode = "ACTIVE", bounciness = 0.1,
					collision_shape = "MESH"):
# mode: "ACTIVE" or "PASSIVE"
# How 'bouncy' an object is. Between 0 and 1

    if mode != "ACTIVE" and mode != "PASSIVE":
        print("Error. mode can only be set to \"ACTIVE\" or \"PASSIVE\"")
        return -1
    if not 0 <= bounciness <= 1:
        print("Error. bounciness must be between 0 and 1")
        return -1

    select_objects([object_name])
    bpy.ops.rigidbody.object_add()
    bpy.context.object.rigid_body.type = mode
    if mode == "ACTIVE":
        bpy.context.object.rigid_body.collision_shape = collision_shape
        bpy.context.object.rigid_body.restitution = bounciness
