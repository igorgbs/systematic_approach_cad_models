import bpy
import numpy as np
import os

from utils_scene import *
from params_scene import *

node_placement_units = np.array([200, 100])

def create_basic_material(name, RGB_diffuse, RGB_glossy,
                          roughness_diffuse, roughness_glossy, mix_factor):

    mat = bpy.data.materials.new(name = name)
    mat.use_nodes = True
    mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))

    ### Material output
    mat_node = mat.node_tree.nodes.get('Material Output')
    mat_node.location = [0,0]

    ### Shaders
    mix_node = mat.node_tree.nodes.new(type = "ShaderNodeMixShader")
    mix_node.location = [-1, 0] * node_placement_units
    mix_node.inputs['Fac'].default_value = mix_factor

    diffuse_node = mat.node_tree.nodes.new(type = "ShaderNodeBsdfDiffuse")
    diffuse_node.location = [-2, 1] * node_placement_units
    RGB_diffuse.append(1)
    diffuse_node.inputs['Color'].default_value = RGB_diffuse
    diffuse_node.inputs['Roughness'].default_value = roughness_diffuse

    glossy_node = mat.node_tree.nodes.new(type = "ShaderNodeBsdfGlossy")
    glossy_node.location = [-2, -2] * node_placement_units
    RGB_glossy.append(1)
    glossy_node.inputs['Color'].default_value = RGB_glossy
    glossy_node.inputs['Roughness'].default_value = roughness_glossy

    mat.node_tree.links.new(mat_node.inputs[0], mix_node.outputs[0])
    mat.node_tree.links.new(mix_node.inputs[1], diffuse_node.outputs[0])
    mat.node_tree.links.new(mix_node.inputs[2], glossy_node.outputs[0])

def create_random_material_support(name):

    RGB_diffuse = [np.random.uniform(support_rgb_range[i][0],
                                     support_rgb_range[i][1]) for i in range(3)]
    RGB_glossy = [np.random.rand() for _ in range(3)]
    # min_val_diffuse = np.random.rand() * 0.6
    # RGB_diffuse = [min_val_diffuse + np.random.rand() * 0.2 for _ in range(3)]
    # rgb_glossy_val = np.random.rand()
    # RGB_glossy = [rgb_glossy_val for _ in range(3)]
    roughness_diffuse = np.random.uniform(support_rough_diffuse_range[0],
                                          support_rough_diffuse_range[1])
    roughness_glossy = np.random.uniform(support_rough_glossy_range[0],
                                         support_rough_glossy_range[1])
    mix_factor = np.random.uniform(support_mixFactor_range[0], support_mixFactor_range[1])

    create_basic_material(name, RGB_diffuse, RGB_glossy, roughness_diffuse, roughness_glossy, mix_factor)

def create_label_mat():

    mat = bpy.data.materials.new(name = "label")
    mat.use_nodes = True
    mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))

    ### Material output
    mat_node = mat.node_tree.nodes.get('Material Output')

    ### Shaders
    emi_node = mat.node_tree.nodes.new(type = "ShaderNodeEmission")
    emi_node.inputs['Color'].default_value = [1,0,0,1]
    emi_node.inputs["Strength"].default_value = 20

    mat.node_tree.links.new(mat_node.inputs[0], emi_node.outputs[0])

def set_material_from_name(obj_name, mat_name):

    select_objects([obj_name])
    obj = bpy.context.selected_objects[0]
    obj.data.materials.clear()
    obj.data.materials.append(bpy.data.materials[mat_name])

def set_material_from_path(obj_name, texture_path):
# Be careful, the folder for the texture cannot contain several files containing a similar keyword.
# List of keywords: REFL, COL, GLOSS, DISP, NRM

    select_objects([obj_name])
    obj = bpy.context.selected_objects[0]
    obj.data.materials.clear()

    mat_name = texture_path.split("/")[-2]
    if mat_name in [bpy.data.materials[i].name for i in range(len(bpy.data.materials))]:
        obj.data.materials.append(bpy.data.materials[mat_name])
    else:
        mat = bpy.data.materials.new(name = mat_name)
        mat.use_nodes = True
        mat.node_tree.nodes.remove(mat.node_tree.nodes.get('Diffuse BSDF'))

        node_placement_units = np.array([200, 100])

        ### Material output
        mat_node = mat.node_tree.nodes.get('Material Output')
        mat_node.location = [0,0]

        ### Shaders
        mix_node = mat.node_tree.nodes.new(type = "ShaderNodeMixShader")
        mix_node.location = [-1, 0] * node_placement_units
        diffuse_node = mat.node_tree.nodes.new(type = "ShaderNodeBsdfDiffuse")
        diffuse_node.location = [-2, 1] * node_placement_units
        glossy_node = mat.node_tree.nodes.new(type = "ShaderNodeBsdfGlossy")
        glossy_node.location = [-2, -2] * node_placement_units

        mat.node_tree.links.new(mat_node.inputs[0], mix_node.outputs[0])
        mat.node_tree.links.new(mix_node.inputs[1], diffuse_node.outputs[0])
        mat.node_tree.links.new(mix_node.inputs[2], glossy_node.outputs[0])

        ### Textures
        for f in os.listdir(texture_path):
            if "REFL" in f:
                reflection_img = bpy.data.images.load(filepath = texture_path + f)
                reflection_node = mat.node_tree.nodes.new(type = "ShaderNodeTexImage")
                reflection_node.location = [-2, 6] * node_placement_units
                reflection_vect_node = mat.node_tree.nodes.new(type = "ShaderNodeTexCoord")
                reflection_vect_node.location = [-3, 6] * node_placement_units
                reflection_node.image = reflection_img
                reflection_node.color_space = "NONE"

                mat.node_tree.links.new(mix_node.inputs[0], reflection_node.outputs[0])
                mat.node_tree.links.new(reflection_node.inputs[0], reflection_vect_node.outputs[0])

            if "COL" in f:
                color_img = bpy.data.images.load(filepath = texture_path + f)
                color_node = mat.node_tree.nodes.new(type = "ShaderNodeTexImage")
                color_node.location = [-3, 3] * node_placement_units
                color_vect_node = mat.node_tree.nodes.new(type = "ShaderNodeTexCoord")
                color_vect_node.location = [-4, 3] * node_placement_units
                color_node.image = color_img

                mat.node_tree.links.new(diffuse_node.inputs[0], color_node.outputs[0])
                mat.node_tree.links.new(color_node.inputs[0], color_vect_node.outputs[0])


            if "GLOSS" in f:
                glossCol_img = bpy.data.images.load(filepath = texture_path + f)
                glossCol_node = mat.node_tree.nodes.new(type = "ShaderNodeTexImage")
                glossCol_node.location = [-3, -4] * node_placement_units
                glossCol_vect_node = mat.node_tree.nodes.new(type = "ShaderNodeTexCoord")
                glossCol_vect_node.location = [-4, -4] * node_placement_units
                glossCol_node.image = glossCol_img

                mat.node_tree.links.new(glossy_node.inputs[0], glossCol_node.outputs[0])
                mat.node_tree.links.new(glossCol_node.inputs[0], glossCol_vect_node.outputs[0])

            if "DISP" in f:
                displacement_img = bpy.data.images.load(filepath = texture_path + f)
                displacement_node = mat.node_tree.nodes.new(type = "ShaderNodeTexImage")
                displacement_node.location = [-1, -6] * node_placement_units
                displacement_vect_node = mat.node_tree.nodes.new(type = "ShaderNodeTexCoord")
                displacement_vect_node.location = [-2, -6] * node_placement_units
                displacement_node.image = displacement_img
                displacement_node.color_space = "NONE"

                mat.node_tree.links.new(mat_node.inputs[2], displacement_node.outputs[0])
                mat.node_tree.links.new(displacement_node.inputs[0], displacement_vect_node.outputs[0])


            if "NRM" in f:
                normal_img = bpy.data.images.load(filepath = texture_path + f)
                normal_shader_node = mat.node_tree.nodes.new(type = "ShaderNodeNormalMap")
                normal_shader_node.location = [-3.5, -0.5] * node_placement_units
                normal_node = mat.node_tree.nodes.new(type = "ShaderNodeTexImage")
                normal_node.location = [-4.5, -0.5] * node_placement_units
                normal_vect_node = mat.node_tree.nodes.new(type = "ShaderNodeTexCoord")
                normal_vect_node.location = [-5.5, -0.5] * node_placement_units
                normal_node.image = normal_img
                normal_node.color_space = "NONE"

                mat.node_tree.links.new(normal_shader_node.inputs[1], normal_node.outputs[0])
                mat.node_tree.links.new(diffuse_node.inputs[2], normal_shader_node.outputs[0])
                mat.node_tree.links.new(glossy_node.inputs[2], normal_shader_node.outputs[0])
                mat.node_tree.links.new(normal_node.inputs[0], normal_vect_node.outputs[0])

        obj.data.materials.append(mat)
