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

    global images_list
    images_list = []

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

    lista_string = list(range(0, 274, 1)) #amount of xml_files + 1
    x = 0
    

    for f in range(len(IMAGE)):

        path_to_img = os.path.join(path,IMAGE[f])
        image = cv2.imread(path_to_img)
        image_expanded = np.expand_dims(image, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        '''
        count_ocurr = xml_list_names.count(IMAGE[f])
        #print("count_ocurr: ", IMAGE[f], count_ocurr)
        for i in range(count_ocurr):
            #print("i: ", i)
            #print("f: ", f)
            #print("xml_list[f+i]: ", xml_list[f+i+x])
            all_ground_truth = np.vstack([all_ground_truth, xml_list[f+i+x][1:]])
        #print("all_ground_truth: \n", all_ground_truth)
        '''
        for i, j in zip(range(boxes.shape[1]), lista_string):

            if scores[0,i] > threshold_scores:

                #predctions values
                ymin_pred = boxes[0,i,0] * height
                xmin_pred = boxes[0,i,1] * width
                ymax_pred = boxes[0,i,2] * height
                xmax_pred = boxes[0,i,3] * width

                #str(int(ymin_pred)) 
                #str(int(xmin_pred)) 
                #str(int(ymax_pred)) 
                #str(int(xmax_pred))
                scores_num = '{0:.10f}'.format(scores[0,i])
                scores_str = str(scores_num)
                
                name = IMAGE[f].split(".")
                name_1 = name[0]
                name_2 = name[0] + ".txt"

                value_pred = [name_2, "volkswagen_logo", scores_str, str(int(xmin_pred)), str(int(ymin_pred)), str(int(xmax_pred)), str(int(ymax_pred))] #add score referente ao xmin, ymin, xmax, ymax
                
                pred_labels_list.append(value_pred) 
                print(value_pred)

                #value_pred_num = [int(xmin_pred), int(ymin_pred), int(xmax_pred), int(ymax_pred)]
                #all_predictions = np.vstack([all_predictions, value_pred_num])
    
              
    with open('/home/igor/Documentos/luigy/Test18/output_all_synthetic.txt', 'w') as f:
        for item in pred_labels_list:
            f.write("%s\n" % item)
    


teste = sys.argv[1]

# MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test4_6.pb
#eval_models_general(xml_path, MODEL_NAME, path, PATH_TO_LABELS, threshold_scores, threshold_boxes-IoU, width, height)


#Hybrid
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test15_Hybrid_5.pb label_map_6
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/TestHybrid_4.pb label_map
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test18_Hybrid_9.pb label_map_9
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test17_Hybrid_1.pb label_map_8
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test12_Hybrid_7.pb label_map_3

#Real
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test15_Real_6.pb label_map_6
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/TestReal_3.pb label_map
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test18_Real_5.pb label_map_9
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test17_Real_5.pb label_map_8
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test12_Real_9.pb label_map_3

#Synthetic
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Experiment_Plan/TensorFlow/trained-inference-graphs/Test12_5.pb label_map_6
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test4_6.pb label_map
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test18_1.pb label_map_9
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test17_1.pb label_map_8
# OK MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test12_1.pb label_map_3


eval_models_general('/home/igor/Documentos/luigy/Test18/groundtruth/*.xml', teste, '/home/igor/Documentos/luigy/Test18/img', '/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/annotations/label_map_9.pbtxt', 0, 0.5, 1280, 720)
