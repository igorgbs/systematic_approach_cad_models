import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from get_iou import *

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")

# Import utilites
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util


def eval_models(xml_path, MODEL_NAME, path, PATH_TO_LABELS, threshold_scores, threshold_boxes, width, height, image_path_draw):
    global xml_list
    xml_list = []
    for xml_file in glob.glob(xml_path):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = [root.find('filename').text, int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)]
            xml_list.append(value)
            #print(value)

    xml_list.sort()


    # Name of the directory containing the object detection module we're using
    #MODEL_NAME = '../TensorFlow/trained-inference-graphs/output_inference_graph_v1.pb'

    # Name of the directory containing all images to be predicted
    #path = '/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all'

    PATH_TO_IMAGE = []
    global IMAGE
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
    #PATH_TO_LABELS = os.path.join(CWD_PATH,'../TensorFlow/annotations','label_map.pbtxt')



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


    # width = 2590
    # height = 1942

    #score draw boxes
    #threshold_scores = 0.5
    #score IoU
    #threshold_boxes = 0.6

    global pred_labels_list
    pred_labels_list = []
    global result_list
    result_list = []
    global result_num_list
    result_num_list = []
    FP, TP, FN = 0, 0, 0
    lista_string = list(range(1, 360, 1))
    for f in range(len(IMAGE)):
        path_to_img = os.path.join(path,IMAGE[f])
        image = cv2.imread(path_to_img)
        image_expanded = np.expand_dims(image, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        tp, fp, fn = 0, 0, 0
        count_detection = 0

        for i, j in zip(range(boxes.shape[1]), lista_string):

            if scores[0,i] >= threshold_scores:
                count_detection += 1
                ymin_pred = boxes[0,i,0] * height
                xmin_pred = boxes[0,i,1] * width
                ymax_pred = boxes[0,i,2] * height
                xmax_pred = boxes[0,i,3] * width

                print("xmin_pred: ", xmin_pred)
                print("ymin_pred: ", ymin_pred)
                print("xmax_pred: ", xmax_pred)
                print("ymax_pred: ", ymax_pred)

                value_pred = [IMAGE[f], int(xmin_pred), int(ymin_pred), int(xmax_pred), int(ymax_pred)] #add score referente ao xmin, ymin, xmax, ymax
                pred_labels_list.append(value_pred)

                xmin_gt = xml_list[f][1]
                ymin_gt = xml_list[f][2]
                xmax_gt = xml_list[f][3]
                ymax_gt = xml_list[f][4]

                iou = get_iou([xmin_gt, ymin_gt, xmax_gt, ymax_gt], [xmin_pred, ymin_pred, xmax_pred, ymax_pred])

                if iou >= threshold_boxes:
                    tp+=1
                if iou < threshold_boxes:
                    fp+=1

                result = [IMAGE[f], iou]

                result_num_list.append(iou)

                result_list.append(result)

                # Draw boxes and save them (Optional) - Has to be improved

                filename_string = str(j) + '_' + IMAGE[f]

                cv2.rectangle(image, (int(xmin_gt), int(ymin_gt)), (int(xmax_gt), int(ymax_gt)), (0, 255, 0), 2)
                cv2.rectangle(image, (int(xmin_pred), int(ymin_pred)), (int(xmax_pred), int(ymax_pred)), (0, 0, 255), 2)

                cv2.putText(image, "IoU: {:.4f}".format(iou), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                print("{}: {:.4f}".format(path_to_img, iou))
                image_path_save = os.path.join(image_path_draw, filename_string)
                cv2.imwrite(image_path_save, image)


        if fp == count_detection:
            fn+=1
        FN+=fn
        FP+=fp
        TP+=tp

    precision = TP / ( TP + FP ) * 100
    recall = TP / ( TP + FN ) * 100
    iou_average = sum(result_num_list) / len(result_num_list) * 100

    #return precision
    #return recall
    #return iou_average

    #print("\nPrecision: ", precision, "%")
    #print("\nRecall: ", recall, "%")
    #print("\nIoU Average: ", iou_average, "%")
    #print("\nResult")
