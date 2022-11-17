data_dir = "/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/blender_generation/blender-2.79/DATA/"

# Floor
path_textures_floor = data_dir + "Textures_lib/Floor/"
floor_dimensions = [5000, 5000, 1]

# Support
support_dim_range = [[100, 200], [300, 400]]
p_realistic_support = 0.5
path_textures_support = data_dir + "Textures_lib/Support/"
support_rgb_range = [[0.6, 0.8], [0.6, 0.8], [0.6, 0.8]]
support_rough_diffuse_range = [0.8, 1]
support_rough_glossy_range = [0.8, 1]
support_mixFactor_range = [0, 0.1]

# Main object
path_main_obj = data_dir + "Obj_lib/"
name_main_obj = "volkswagen_logo"
n_primary_range = [1,2] #[n_min, n_max + 1], for example to get a random number of objects between 1 and 5: [1, 6]


# Distractors -> Other STL Files
path_distractors = data_dir + "STL_lib/"
path_textures_distractors = data_dir + "Textures_lib/Objects/"
n_distractors_max = 20
distractors_rot_range = [[-30, 30], [-30, 30], [-30, 30]]
distractors_pos_range_z = [100, 200]

# Lights
max_n_lights = 4
n_lights_probas = [0.4, 0.3, 0.2, 0.1]

# Physics
max_n_frames_physics = 2000
