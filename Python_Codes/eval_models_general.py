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


def eval_models_general(xml_path, MODEL_NAME, path, PATH_TO_LABELS, threshold_scores, threshold_boxes, width, height):

    global xml_list
    xml_list = []
    for xml_file in glob.glob(xml_path):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            xmin_xml = int(member[4][0].text)
            ymin_xml = int(member[4][1].text)
            xmax_xml = int(member[4][2].text)
            ymax_xml = int(member[4][3].text)
            filename_xml = root.find('filename').text
            if xmin_xml != 0 and ymin_xml != 0 and xmax_xml != 0 and ymax_xml != 0:
                value = [filename_xml, xmin_xml, ymin_xml, xmax_xml, ymax_xml]
                xml_list.append(value)
            #value_num = [int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)]
            #all_ground_truth = np.vstack([all_ground_truth, value_num])
            #print(value)
    print(xml_list)        
    #a = ['bresil_ad_blue1_100.png', 1000, 200, 300, 400]
    #xml_list.append(a)
    #b = ['bresil_ad_blue1_100.png', 1100, 500, 400, 900]
    #xml_list.append(b)
    xml_list.sort()

    xml_list_names = []
    for i in xml_list:
        xml_list_names.append(i[0])

    '''
    for i in xml_list:
        all_ground_truth = np.vstack([ all_ground_truth, i[1:] ])

    all_ground_truth = np.delete(all_ground_truth, 0, 0)
    print("\nall_ground_truth")
    print(all_ground_truth)
    '''
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
            if '.jpg' in file:
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

    # width = 705, height = 447
    # width = 2590, height = 1942

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

    global all_predictions
    all_predictions = np.zeros([1,4], dtype = int)
    all_predictions = np.delete(all_predictions, 0, 0)

    global all_ground_truth
    all_ground_truth = np.zeros([1,4], dtype = int)
    all_ground_truth = np.delete(all_ground_truth, 0, 0)

    FP, TP, FN = 0, 0, 0

    lista_string = list(range(0, 379, 1)) #amount of xml_files + 1
    x = 0
    for f in range(len(IMAGE)):

        path_to_img = os.path.join(path,IMAGE[f])
        image = cv2.imread(path_to_img)
        image_expanded = np.expand_dims(image, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})


        count_ocurr = xml_list_names.count(IMAGE[f])
        #print("count_ocurr: ", IMAGE[f], count_ocurr)
        for i in range(count_ocurr):
            #print("i: ", i)
            #print("f: ", f)
            #print("xml_list[f+i]: ", xml_list[f+i+x])
            all_ground_truth = np.vstack([all_ground_truth, xml_list[f+i+x][1:]])
        #print("all_ground_truth: \n", all_ground_truth)


        for i, j in zip(range(boxes.shape[1]), lista_string):

            if scores[0,i] >= threshold_scores:

                #predctions values
                ymin_pred = boxes[0,i,0] * height
                xmin_pred = boxes[0,i,1] * width
                ymax_pred = boxes[0,i,2] * height
                xmax_pred = boxes[0,i,3] * width

                value_pred = [IMAGE[f], int(xmin_pred), int(ymin_pred), int(xmax_pred), int(ymax_pred)] #add score referente ao xmin, ymin, xmax, ymax
                pred_labels_list.append(value_pred)

                value_pred_num = [int(xmin_pred), int(ymin_pred), int(xmax_pred), int(ymax_pred)]
                all_predictions = np.vstack([all_predictions, value_pred_num])



                # Draw boxes and save them (Optional) - Has to be improved
                '''
                filename_string = str(j) + '_' + IMAGE[f]

                cv2.rectangle(image, (int(xmin_gt), int(ymin_gt)), (int(xmax_gt), int(ymax_gt)), (0, 255, 0), 2)
                cv2.rectangle(image, (int(xmin_pred), int(ymin_pred)), (int(xmax_pred), int(ymax_pred)), (0, 0, 255), 2)

                cv2.putText(image, "IoU: {:.4f}".format(iou), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
                print("{}: {:.4f}".format(path_to_img, iou))
                image_path_save = os.path.join(image_path_draw, filename_string)
                cv2.imwrite(image_path_save, image)
                '''

        if all_ground_truth.shape[0] == 0:
            tp = 0
            fn = 0
            fp = all_predictions.shape[0]
        if all_predictions.shape[0] == 0:
            tp = 0
            fn = all_ground_truth.shape[0]
            fp = 0
        else:
            fp, fn, tp = 0, 0, 0
            matrix = np.zeros([all_ground_truth.shape[0], all_predictions.shape[0]])
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    iou = get_iou(all_ground_truth[i], all_predictions[j])
                    result = [IMAGE[f], iou]
                    result_num_list.append(iou)
                    result_list.append(result)
                    if  iou >= threshold_boxes:
                        matrix[i, j] += 1
            sum_rows = matrix.sum(axis = 0)
            sum_cols = matrix.sum(axis = 1)
            for j in range(len(sum_cols)):
                if sum_cols[j] == 0:
                    fn += 1
                if sum_cols[j] == 1:
                    tp += 1
                if sum_cols[j] >= 2:
                    tp += 1
                    fp += sum_cols[j] - 1
            for i in range(len(sum_rows)):
                if sum_rows[i] == 0:
                    fp += 1
        TP += tp
        FP += fp
        FN += fn

        #print("all_predictions of: ", IMAGE[f] , all_predictions)
        n = all_predictions.shape[0]
        all_predictions = all_predictions[:-n, :]

        #print("x: ", x)
        x+=(count_ocurr-1)
        #print("x: ", x)
        m = all_ground_truth.shape[0]
        #print("m: ", m)
        all_ground_truth = all_ground_truth[:-m, :]
        #print("all_ground_truth: ", all_ground_truth)

    precision = round(TP / ( TP + FP ) * 100 , 2)
    recall = round(TP / ( TP + FN ) * 100, 2)
    f1_score = round(2 * ( (precision*recall) / (precision+recall) ), 2)

    #iou_average = sum(result_num_list) / len(result_num_list) * 100

    #return precision
    #return recall
    #return iou_average
    '''
    for i in result_list:
        print(i)
    '''

    print("\n")
    print("TP: ", TP)
    print("FP: ", FP)
    print("FN: ", FN, "\n")

    print("\nPrecision: ", precision, "%")
    print("\nRecall: ", recall, "%")
    print("\nF1-Score: ", f1_score, "%")
    #print("\nIoU Average: ", iou_average, "%")
