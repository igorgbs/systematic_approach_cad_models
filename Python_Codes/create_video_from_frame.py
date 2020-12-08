import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('/home/igor/Documentos/Developments/cad2learn/Object_Detection/training_demo/ad_blue/*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('video_2.avi',cv2.VideoWriter_fourcc(*'MJPG'), 2, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()
