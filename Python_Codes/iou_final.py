import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

threshold = 0.5

xml_list = []
for xml_file in glob.glob('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Fuelcap_Oficial_Images/fuelcap_2_640x480_xml/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member in root.findall('object'):
        value = [root.find('filename').text, int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)]
        xml_list.append(value)
        #print(value)

xml_list.sort()

# Name of the directory containing the object detection module we're using
MODEL_NAME = '/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test17_1.pb'

# Name of the directory containing all images to be predicted
path = '/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Fuelcap_Oficial_Images/fuelcap_2_640x480/'

PATH_TO_IMAGE = []
IMAGE = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.png' in file:
            PATH_TO_IMAGE.append(os.path.join(r, file))
            IMAGE.append(file)

IMAGE.sort()

# Grab path to current working directory
CWD_PATH = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/annotations/','label_map_8.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objectbresil_ad_blue4_0.pngs.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# width = 705, height = 447
# width = 2590, height = 1942
largura = 640
altura = 480

pred_labels_list = []
for f in IMAGE:
    path_to_img = os.path.join(path,f)
    image = cv2.imread(path_to_img)
    image_expanded = np.expand_dims(image, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_expanded})

    ymin = boxes[0,0,0] * altura
    xmin = boxes[0,0,1] * largura
    ymax = boxes[0,0,2] * altura
    xmax = boxes[0,0,3] * largura

    value_pred = [f, int(xmin), int(ymin), int(xmax), int(ymax)]
    pred_labels_list.append(value_pred)
    #print(value_pred)

pred_labels_list.sort()


def get_iou(a, b):

    # a: real image
    # b: predicted image
    # COORDINATES OF THE INTERSECTION BOX / Order: [xmin, ymin, xmax, ymax]
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])

    # AREA OF OVERLAP - Area where the boxes intersect
    width = (x2 - x1)
    height = (y2 - y1)
    # handle case where there is NO overlap
    if (width<0) or (height <0):
        return 0.0
    area_overlap = width * height

    # COMBINED AREA
    area_a = (a[2] - a[0]) * (a[3] - a[1])
    area_b = (b[2] - b[0]) * (b[3] - b[1])
    area_combined = area_a + area_b - area_overlap

    # RATIO OF AREA OF OVERLAP OVER COMBINED AREA
    iou = area_overlap / (area_combined)
    return iou



res_par = []
res_num = []
result = []
for x, y in zip(xml_list, pred_labels_list):

    res_num.append(get_iou(x[1:5], y[1:5]))
    res_par = [x[0:1], get_iou(x[1:5], y[1:5])]
    result.append(res_par)
    print("result: ", result)
    print("x[0]: ", x[0])
    # load the image
    image_path = os.path.join(path, x[0])
    image = cv2.imread(image_path)
    # draw the ground-truth bounding box along with the predicted bounding box
    cv2.rectangle(image, tuple(x[1:3]), tuple(x[3:6]), (0, 255, 0), 2)
    cv2.rectangle(image, tuple(y[1:3]), tuple(y[3:6]), (0, 0, 255), 2)

    # compute the intersection over union and display it
    iou = get_iou(x[1:5], y[1:5])


    cv2.putText(image, "IoU: {:.4f}".format(iou), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    print("{}: {:.4f}".format(image_path, iou))
    image_path_save = os.path.join('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/IoU_Draw/', x[0])
    cv2.imwrite(image_path_save, image)
    print("Saving image: ", x[0])
    #cv2.imshow("Image", image)
	#cv2.waitKey(0)


'''
TP = [c for c in res_num if c >= threshold]
FP = [c for c in res_num if c < threshold]
precision = ( len(TP) ) / ( len(TP) + len(FP) ) * 100
iou_average = sum(res_num) / len(res_num) * 100


print("Precision: ", precision, "%")
print("IoU Average: ", iou_average, "%")
'''
