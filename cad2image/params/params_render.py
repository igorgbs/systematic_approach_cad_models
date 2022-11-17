import bpy

# Camera
clip_end = 10000
distance_range_cam = [300, 1200]
rotation_range_cam = [[0, 75], [0, 360]]
#image resolution
resolution = [int(960), int(540)]

# Device for rendering
rendering_type = "gpu"
gpu_name = "Quadro P5000 (Display)"

bpy.context.scene.render.engine = 'CYCLES'
