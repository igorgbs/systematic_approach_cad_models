import shutil
import os
import glob

#path to source Images Generated with Blender
path_source_Images = '/home/igor/Documentos/Developments/blender_generation/cad2image-master-2/Generated_data/Test16/Images'
path_source_Labels = '/home/igor/Documentos/Developments/blender_generation/cad2image-master-2/Generated_data/Test16/Labels'

#path to destination - Images
path_Test7_Images_Test = '/home/igor/Documentos/Developments/Experiment_Plan/Images_Generated_Blender/Test16_Images_Test'
path_Test7_Labels_Test = '/home/igor/Documentos/Developments/Experiment_Plan/Images_Generated_Blender/Test16_Labels_Test'

#cam_poses = [15,16,17,18,19]
#scene_values = [180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199]

#scene_0__cam_0.png

for image in glob.glob(path_source_Images + '/*.png'):

    image_file = os.path.basename(image)

    for cam in range(5):
        for scene in range(20):
            if str(image_file) == "scene_" + str(scene) + "__cam_" + str(cam) + ".png":
                print("copying...", image_file)
                file_destination_image = os.path.join(path_Test7_Images_Test, image_file)
                shutil.copyfile(image, file_destination_image)


for label in glob.glob(path_source_Labels + '/*.xml'):

    label_file = os.path.basename(label)

    for cam in range(5):
        for scene in range(20):
            if str(label_file) == "scene_" + str(scene) + "__cam_" + str(cam) + ".xml":
                print("copying...", label_file)
                file_destination_label = os.path.join(path_Test7_Labels_Test, label_file)
                shutil.copyfile(label, file_destination_label)
