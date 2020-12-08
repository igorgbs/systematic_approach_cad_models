import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET

sys.path.append("..")

xml_list = []
for xml_file in glob.glob('/home/igor/Documentos/Developments/Experiment_Plan/Renault_Oficial_Images/ad_blue_all_480p_xml/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member, tam in zip(root.findall('object'), root.findall('size')):
        value = [root.find('filename').text, int(tam[0].text), int(tam[1].text), int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text)]
        xml_list.append(value)
        print(value)
