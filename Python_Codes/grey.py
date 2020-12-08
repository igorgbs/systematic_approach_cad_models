import cv2
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

#path = sys.argv[1]
#image_path_save = sys.argv[2]
path = '/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all_480p/'
image_path_save = '/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all_480p_grey/'

PATH_TO_IMAGE = []
IMAGE = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            PATH_TO_IMAGE.append(os.path.join(r, file))
            IMAGE.append(file)

for i, j in zip(PATH_TO_IMAGE, IMAGE):
    bgr_img = cv2.imread(i)
    gray_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    new_image_grey = image_path_save + j
    cv2.imwrite(new_image_grey, gray_img)
    print(new_image_grey, ":", " Successfully saved")
