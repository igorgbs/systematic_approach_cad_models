import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET

from get_iou import *
from eval_models_general import * 


teste = sys.argv[1]
# MODEL_NAME = /media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/trained-inference-graphs/Test17_Hybrid_10.pb
# MODEL_NAME (adblue) = /media/igor/home/igor/Documentos/Developments/Experiment_Plan/TensorFlow/trained-inference-graphs/Test15_Hybrid_10.pb

#eval_models_general(xml_path, MODEL_NAME, path, PATH_TO_LABELS, threshold_scores, threshold_boxes-IoU, width, height)

#NORMAL
#/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Yamaha_Oficial_Images/yamaha_6_640x480_xml/*.xml
#/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Yamaha_Oficial_Images/yamaha_6_640x480/

#OVERFITTING
#/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Images_Generated_Blender/TestReal_1_Labels_Train/*.xml
#/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Images_Generated_Blender/TestReal_1_Images_Train/

eval_models_general('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Fuelcap_Oficial_Images/fuelcap_2_1280x720/*.xml', teste, '/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Fuelcap_Oficial_Images/volkswagen_1_1280x720/', '/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/annotations/label_map_8.pbtxt', 0.6, 0.5, 1280, 720)
