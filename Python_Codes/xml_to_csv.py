import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

format_image='.png'

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text + format_image,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():

    xml_df = xml_to_csv('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Images_Generated_Blender/Test12_Labels_Train')
    xml_df.to_csv('/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/Tensorflow/annotations/Test12_Train.csv', index=None)
    print('Successfully converted xml to csv.')


main()
