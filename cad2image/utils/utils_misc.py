import bpy
import numpy as np
import os, sys
# import cv2
from lxml import etree

from utils_material import *
from utils_scene import *
from utils_render import *

def isAlmostEqualMat(mat1, mat2, thresh):
# Compare if two blender matrices have all their coefficients less than a threshold
# Is used for comparing tranformation matrices
    sizeX, sizeY = len(mat1), len(mat1[0])
    for i in range(sizeX):
        for j in range(sizeY):
            if np.abs(mat1[i][j] - mat2[i][j]) > thresh:
                return False
    return True

def create_bounding_box(resolution, dir_path):

    # create_label_mat()
    # select_objects([object])
    # obj = bpy.context.selected_objects[0]
    # obj.data.materials.clear()
    # obj.data.materials.append(bpy.data.materials["label"])

    render(destination = dir_path + "temp/mask_bb.png", resolution = resolution)

    return compute_bb(dir_path + "temp/mask_bb.png", resolution)

def read_image_RGB(path, resolution):

    height, width = int(resolution[1]), int(resolution[0])
    im = bpy.data.images.load(path)
    im = np.array(im.pixels[:])

    mask = np.zeros([height, width, 3])

    for ih in range(height):
        for iw in range(width):
            for ic in range(4):
                n = ih * 4 * width + iw * 4 + ic
                if ic != 3:
                    mask[height - 1 - ih, iw, ic] = im[n] * 255

    return mask

def compute_bb(mask_path, resolution):

    mask = read_image_RGB(mask_path, resolution)

    tot_pix_img = resolution[0] * resolution[1]
    if np.argwhere(mask[:, :, 0] > 100).shape[0] * 100 / tot_pix_img < 0.05:
        return -1

    top = np.min(np.argwhere(mask[:, :, 0] > 100)[:, 0])
    left = np.min(np.argwhere(mask[:, :, 0] > 100)[:, 1])

    bottom = np.max(np.argwhere(mask[:, :, 0] > 100)[:, 0])
    right = np.max(np.argwhere(mask[:, :, 0] > 100)[:, 1])

    BB = [left, top, right, bottom]

    return BB

# def compute_bb(mask_path):
#
#     mask = cv2.imread(mask_path)
#     mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
#
#     top = np.min(np.argwhere(mask[:, :, 0] > 100)[:, 0])
#     left = np.min(np.argwhere(mask[:, :, 0] > 100)[:, 1])
#
#     bottom = np.max(np.argwhere(mask[:, :, 0] > 100)[:, 0])
#     right = np.max(np.argwhere(mask[:, :, 0] > 100)[:, 1])
#
#     BB = [left, top, right, bottom]
#
#     return BB

def make_description_file(filename_, path_, database_, width_, height_, depth_ = 3,
                        segmented_ = 0, classe_ = ["class0"], pose_ = 'Unspecified',
                        truncated_ = '0', difficult_ = '0', xmin_ = [-1], ymin_ = [-1],
                        xmax_ = [-1], ymax_ = [-1], path_labels = "./"):

    folder_path = os.path.dirname(path_)

    #Pascal Label Architecture
    annotation = etree.Element("annotation")
    folder = etree.SubElement(annotation, "folder")
    filename = etree.SubElement(annotation, "filename")
    path = etree.SubElement(annotation, "path")

    source = etree.SubElement(annotation, "source")
    database = etree.SubElement(source, "database")

    size =  etree.SubElement(annotation, "size")
    width = etree.SubElement(size, "width")
    height = etree.SubElement(size, "height")
    depth = etree.SubElement(size, "depth")

    segmented = etree.SubElement(annotation, "segmented")
    for k in range(len(xmin_)):
        for i in range(len(classe_)):
            object = etree.SubElement(annotation, "object")
            etree.SubElement(object, "name").text = classe_[i]
            etree.SubElement(object, "pose").text = pose_
            etree.SubElement(object, "truncated").text = truncated_
            etree.SubElement(object, "difficult").text = difficult_

            bndbox = etree.SubElement(object, "bndbox")
            etree.SubElement(bndbox, "xmin").text = str(xmin_[k][i])
            etree.SubElement(bndbox, "ymin").text = str(ymin_[k][i])
            etree.SubElement(bndbox, "xmax").text = str(xmax_[k][i])
            etree.SubElement(bndbox, "ymax").text = str(ymax_[k][i])

    #Set of the value
    folder.text = os.path.basename(folder_path)
    filename.text = filename_
    path.text = path_
    database.text = database_
    width.text = str(width_)
    height.text = str(height_)
    depth.text = str(depth_)
    segmented.text = str(segmented_)


    #Create the label
    name_label, file_extension = os.path.splitext(filename_)

    my_tree = etree.ElementTree(annotation)

    file = open(path_labels + name_label + ".xml",'wb')
    file.write(etree.tostring(my_tree, pretty_print=True))
    file.close()

def Prepare_generatedDataset_dir(path_generated_data, generated_dataset_basename):

    if not os.path.isdir(path_generated_data):
        os.mkdir(path_generated_data)

    dataset_exists = True
    k = 0
    generated_dataset_name = generated_dataset_basename[:]
    while dataset_exists:
        if os.path.isdir(path_generated_data + generated_dataset_name):
            generated_dataset_name = generated_dataset_basename + "_%i" % k
            k += 1
        else:
            os.mkdir(path_generated_data + generated_dataset_name)
            os.mkdir(path_generated_data + generated_dataset_name + "/Images")
            os.mkdir(path_generated_data + generated_dataset_name + "/Labels")
            dataset_exists = False

    return generated_dataset_name
