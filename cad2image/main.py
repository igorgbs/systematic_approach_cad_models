from lxml import etree

import bpy
import numpy as np
import copy
import sys, os
import time

tstart = time.time()

#dir_path = "/home/joris/Isabo/Code/Development/Blender/cad2image/"
#dir_path = "/home/jorisguerin/Code/cad2image/"
dir_path = "/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/blender_generation/blender-2.79/"

sys.path.append(dir_path + "utils/")
sys.path.append(dir_path + "params/")

from utils_scene import *
from utils_light import *
from utils_physics import *
from utils_material import *
from utils_render import *
from utils_misc import *

from params_scene import *
from params_general import *

###############################
### Prepare to save dataset ###
###############################

generated_dataset_name = Prepare_generatedDataset_dir(path_generated_data,
                                                      generated_dataset_basename)

path_generated_images = path_generated_data + generated_dataset_name + "/Images/"
path_generated_labels = path_generated_data + generated_dataset_name + "/Labels/"

#################
### Constants ###
#################

base_distractor_name = "dist"
secSourceList = [add_spotLight, add_pointLight]

###############################
### Start generating scenes ###
###############################

for i_scn in range(n_scenes):
    clear_scene()
    add_cam()

    ########################################
    ### Generate random scene parameters ###
    ########################################

    # Cameras
    all_cam_poses = [random_cam_pose() for i in range(n_cam_poses_per_scene)]

    # Support
    support_dimensions = [np.random.randint(support_dim_range[0][0], support_dim_range[0][1]),
                          np.random.randint(support_dim_range[1][0], support_dim_range[1][1]),
                          1]
    realistic_support = np.random.rand() < p_realistic_support
    if realistic_support:
        texture_sprt = np.random.choice(os.listdir(path_textures_support))
        support_texture_path = path_textures_support + texture_sprt + "/"

    # Floor
    texture_flr = np.random.choice(os.listdir(path_textures_floor))
    floor_texture_path = path_textures_floor + texture_flr + "/"

    # Distractors
    
    #n_distractors = np.random.randint(0, n_distractors_max)
    n_distractors = 20
    distractors_textures_path = []
    for i in range(n_distractors):
        texture_dist = np.random.choice(os.listdir(path_textures_distractors))
        distractors_textures_path.append(path_textures_distractors + texture_dist + "/")
    
    # Light
    n_secLight = np.random.choice(range(max_n_lights), p = n_lights_probas)
    sec_lights = []
    for _ in range(n_secLight):
        sec_lights.append(np.random.choice(secSourceList))

    ######################
    ### Floor creation ###
    ######################

    floor = bpy.ops.mesh.primitive_plane_add(radius=1, location=(0, 0, -1000))
    bpy.ops.transform.resize(value = floor_dimensions)
    obj = bpy.context.selected_objects[0]
    obj.name = "floor"

    activate_physics("floor", "PASSIVE")

    ########################
    ### Support creation ###
    ########################

    support = bpy.ops.mesh.primitive_plane_add(radius=1, location=(0, 0, 10))
    bpy.ops.transform.resize(value = support_dimensions)
    obj = bpy.context.selected_objects[0]
    obj.name = "support"

    activate_physics("support", "PASSIVE")

    ################################
    ### Primary objects creation ###
    ################################
# This part of the code is dependant on the studied object.
# This example is specific to the ADblue image generation problem.
# For each new object studied, this part should be modified according to the use case.
    n_prim_obj = np.random.randint(*n_primary_range)
    prvtrslts = [[1e5, 1e5, 1e5]]
    obj_parts_names = []
    for i_obj in range(n_prim_obj):
        bpy.ops.import_scene.obj(filepath = path_main_obj + name_main_obj + ".obj")

        min_dist = 1.2 * np.max([bpy.context.selected_objects[0].dimensions[0], bpy.context.selected_objects[0].dimensions[2]])

        obj_parts_names.append([])
        for i in range(len(bpy.context.selected_objects)):
            bpy.context.selected_objects[i].name = bpy.context.selected_objects[i].name.split("_Shape")[0] + "_" + str(i_obj)
            obj_parts_names[-1].append(bpy.context.selected_objects[i].name)

        while True:
            translates = [np.random.uniform(-support_dimensions[0]/4, support_dimensions[0]/4),
                          np.random.uniform(-support_dimensions[1]/4, support_dimensions[1]/4),
                          np.random.uniform(10, 20)]
            dists = [np.linalg.norm(np.array(translates[:2]) - np.array(prvtrslts[k][:2])) for k in range(len(prvtrslts))]
            if np.min(dists) > min_dist:
                break

        prvtrslts.append(translates)

        bpy.ops.object.select_all(action='DESELECT')
        select_objects(obj_parts_names[-1])

        bpy.ops.transform.translate(value = translates)

        bpy.ops.object.select_all(action='DESELECT')
        select_objects(obj_parts_names[-1])
        bpy.ops.rigidbody.objects_add()
        objs = bpy.context.selected_objects
        objs[0].rigid_body.type = "PASSIVE"
        #objs[1].rigid_body.type = "PASSIVE"
        #objs[2].rigid_body.type = "PASSIVE"
    
    ##################################
    ### Secondary objects creation ###
    ##################################
    #Distractors
    
    for i in range(n_distractors):

        model_dist = np.random.choice(os.listdir(path_distractors))
        distractor_model = path_distractors + model_dist

        import_mesh(distractor_model, base_distractor_name + str(i), texture_path = None,
                initial_location = [np.random.randint(-support_dimensions[0] / 3, support_dimensions[0] / 3),
                                    np.random.randint(-support_dimensions[1] / 3, support_dimensions[1] / 3),
                                    np.random.randint(distractors_pos_range_z[0], distractors_pos_range_z[1])],
    			initial_rotation = [np.deg2rad(np.random.randint(distractors_rot_range[k][0], distractors_rot_range[k][1])) for k in range(3)])

        bpy.ops.object.shade_smooth()
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].split_angle = np.deg2rad(20)

        activate_physics(base_distractor_name + str(i), collision_shape = "CONVEX_HULL")
    
    ###################
    ### Run physics ###
    ###################

    bpy.context.scene.rigidbody_world.point_cache.frame_end = max_n_frames_physics
    select_objects([base_distractor_name + str(i) for i in range(n_distractors)])

    bpy.context.scene.frame_set(1)
    n_frames = 0
    isMoving = True
    prev_loc = copy.deepcopy([bpy.data.objects[base_distractor_name + str(i)].matrix_world for i in range(n_distractors)])

    while isMoving:
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        n_frames += 1
        if n_frames % 10 == 0:
            cur_loc = copy.deepcopy([bpy.data.objects[base_distractor_name + str(i)].matrix_world for i in range(n_distractors)])
            isMoving = False
            for i in range(len(cur_loc)):
                if not isAlmostEqualMat(cur_loc[i], prev_loc[i], 1e-2):
                    isMoving = True
                    break
            prev_loc = cur_loc[:]
        if n_frames > max_n_frames_physics:
            isMoving = False
    
    ###############################
    ### generate bounding boxes ###
    ###############################

    ## Set materials
    create_basic_material("label_black", RGB_diffuse = [70, 70, 0], RGB_glossy = [0, 0, 0],
                          roughness_diffuse = 1, roughness_glossy = 1, mix_factor = 1)
    create_label_mat()

    set_material_from_name("floor", "label_black")
    set_material_from_name("support", "label_black")

    #Distractors
    
    for i in range(n_distractors):
        set_material_from_name(base_distractor_name + str(i), "label_black")
    
    bounding_boxes = []
    for k in range(len(obj_parts_names)):
        bounding_boxes.append([])
        set_material_from_name(obj_parts_names[k][0], "label")
        for j in range(len(obj_parts_names)):
            if j != k:
                set_material_from_name(obj_parts_names[j][0], "label_black")
                set_material_from_name(obj_parts_names[j][1], "label_black")
        ## Save mask and compute bb
        if not os.path.isdir(dir_path + "temp"):
            os.mkdir(dir_path + "temp/")

        use_cam_pose = [1 for i in range(n_cam_poses_per_scene)]
        for i_cam in range(len(all_cam_poses)):
            bpy.data.objects["Camera"].location = all_cam_poses[i_cam][0]
            bpy.data.objects["Camera"].rotation_euler = all_cam_poses[i_cam][1]

            bounding_boxes[-1].append(create_bounding_box(resolution, dir_path))

    for i_cam in range(len(all_cam_poses)):
        fname = "scene_%i__cam_%i" % (i_scn, i_cam)
        xmin, xmax, ymin, ymax = [], [], [], []
        for i in range(n_prim_obj):
            if bounding_boxes[i][i_cam] == -1:
                use_cam_pose[i_cam] = 0
            else:
                xmin.append([bounding_boxes[i][i_cam][0]])
                ymin.append([bounding_boxes[i][i_cam][1]])
                xmax.append([bounding_boxes[i][i_cam][2]])
                ymax.append([bounding_boxes[i][i_cam][3]])
        if xmin != []:
            make_description_file(filename_ = fname, path_ = path_generated_images,
                                  database_ = generated_dataset_name,
                                  width_ = resolution[0], height_ = resolution[1],
                                  classe_ = [name_main_obj],
                                  xmin_ = xmin, ymin_ = ymin, xmax_ = xmax, ymax_ = ymax,
                                  path_labels = path_generated_labels)
        else:
            make_description_file(filename_ = fname, path_ = path_generated_images,
                                  database_ = generated_dataset_name,
                                  width_ = resolution[0], height_ = resolution[1],
                                  classe_ = [name_main_obj],
                                  xmin_ = [[0]], ymin_ = [[0]], xmax_ = [[0]], ymax_ = [[0]],
                                  path_labels = path_generated_labels)

    ################################
    ### Setting render materials ###
    ################################

    ## Floor
    set_material_from_path("floor", floor_texture_path)

    ## Support
    if realistic_support:
        set_material_from_path("support", support_texture_path)
    else:
        create_random_material_support("mat_sup")
        set_material_from_name("support", "mat_sup")

    ## Primary object
# This section is specific to the object of study. For example, here, the adblue has first been manually preprocessed to
# select the faces which need to be white and blue and saved has a .obj object. The colors are designed manually.
# RGB diffuse set the real color of the object. Check Blender to see what the pattern of colors.
    create_basic_material("grey", RGB_diffuse = [0.352, 0.337, 0.305], RGB_glossy = [1, 1, 1],
                          roughness_diffuse = 1, roughness_glossy = 1, mix_factor = 0.1)
    for j in range(len(obj_parts_names)):
        select_objects([obj_parts_names[j][0]])
        obj = bpy.context.selected_objects[0]
        obj.data.materials.clear()
        obj.data.materials.append(bpy.data.materials["grey"])
    
    '''  
    create_basic_material("grey", RGB_diffuse = [0.216, 0.216, 0.216], RGB_glossy = [0.8, 0.8, 0.8],
                          roughness_diffuse = 1, roughness_glossy = 0.925, mix_factor = 0.02)
    
    for j in range(len(obj_parts_names)):
        select_objects([obj_parts_names[j][1]])
        obj = bpy.context.selected_objects[0]
        obj.data.materials.clear()
        obj.data.materials.append(bpy.data.materials["grey"])


    create_basic_material("label_black", RGB_diffuse = [0.02, 0.02, 0.02], RGB_glossy = [0.8, 0.8, 0.8],
                          roughness_diffuse = 1, roughness_glossy = 0.925, mix_factor = 0.02)

    for j in range(len(obj_parts_names)):
        select_objects([obj_parts_names[j][2]])
        obj = bpy.context.selected_objects[0]
        obj.data.materials.clear()
        obj.data.materials.append(bpy.data.materials["label_black"])    
    '''
    ## Distractors
    
    prob = 0.1
    for i in range(n_distractors):
        distractor_name = base_distractor_name + str(i)
        if np.random.rand() < prob:
            set_material_from_name(distractor_name, "label_black")
        else:
            set_material_from_path(base_distractor_name + str(i), distractors_textures_path[i])
    
    ########################
    ### Light management ###
    ########################

    ## Primary light source ##
    ##########################
    add_sunLight()

    ## Secondary light source ##
    ############################
    for sl in sec_lights:
        sl()

    #################
    ### Rendering ###
    #################
    if isRender == True:
        for i_cam in range(len(all_cam_poses)):
            #if use_cam_pose[i_cam] == 1:
            fname = "scene_%i__cam_%i" % (i_scn, i_cam)

            bpy.data.objects["Camera"].location = all_cam_poses[i_cam][0]
            bpy.data.objects["Camera"].rotation_euler = all_cam_poses[i_cam][1]
            render(destination = path_generated_images + fname + ".png", resolution = resolution)

print("Generation Time: ", time.time()-tstart, "sec")
