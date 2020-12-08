import numpy as np
import os
import glob
import xml.etree.ElementTree as ET


rate_x = 1280/640
rate_y = 720/480
new_width = 640
new_height = 480
xml_list = []
for xml_file in glob.glob('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Volkswagen_Oficial_Images/volkswagen_1_inference_640x480_xml/*.xml'):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for member, tam in zip(root.findall('object'), root.findall('size')):
        new_xmin = int(round(int(member[4][0].text) / rate_x , 0))
        new_ymin = int(round(int(member[4][1].text) / rate_y , 0))
        new_xmax = int(round(int(member[4][2].text) / rate_x , 0))
        new_ymax = int(round(int(member[4][3].text) / rate_y , 0))

        print("\n")
        print("new_xmin: ", new_xmin)
        print("new_ymin: ", new_ymin)
        print("new_xmax: ", new_xmax)
        print("new_ymax: ", new_ymax)
        print("new_width: ", new_width)
        print("new_height: ", new_height)

        int(round(new_xmin,0))

        member[4][0].text = str(new_xmin)
        member[4][1].text = str(new_ymin)
        member[4][2].text = str(new_xmax)
        member[4][3].text = str(new_ymax)
        tam[0].text = str(new_width)
        tam[1].text = str(new_height)

    tree.write(xml_file)
