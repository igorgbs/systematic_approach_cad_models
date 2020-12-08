import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import glob
import pandas as pd
import xml.etree.ElementTree as ET


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



word1 = 'igor'
word2 = 'nayne'
txt_name = "/media/igor/home/igor/Documentos/Developments/Yamaha_Experiment_Plan/luigy/predictions/output.txt"

f = open(txt_name, 'w')
print(word1, word2, file=f )
