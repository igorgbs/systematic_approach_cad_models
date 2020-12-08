import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_txt(path):
    #xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            name = root.find('filename').text.split(".")
            name_2 = name[0]
            txt_name = path + name_2 + ".txt"       
            '''
            value = (member[0].text, 
                    str(member[4][0].text), 
                    str(member[4][3].text), 
                    str(member[4][2].text), 
                    str(member[4][1].text)
                )
            '''
            f = open(txt_name, 'w')
            f.write('{0} {1} {2} {3} {4} \n'.format(member[0].text, str(member[4][0].text), str(member[4][3].text), str(member[4][2].text), str(member[4][1].text)))
            f.close()    

def main():

    xml_txt = xml_to_txt('/home/igor/Documentos/luigy/Test18/groundtruth/')
    print('Successfully converted xml to txt.')

main()
