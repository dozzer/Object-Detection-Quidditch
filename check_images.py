from xml.etree import ElementTree
from glob import glob as xmlFiles

from urllib.request import urlopen
import os

import numpy as np
import cv2
from matplotlib import pyplot as plt

# %matplotlib inline

ann_folder = "ann"
img_folder = "images"

BOX_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)


def visualize_bbox(img, bbox, class_id, class_idx_to_name, color=BOX_COLOR, thickness=2):
    x_min, y_min, w, h = bbox
    x_min, x_max, y_min, y_max = int(x_min), int(x_min + w), int(y_min), int(y_min + h)
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color=color, thickness=thickness)
    class_name = class_idx_to_name[class_id]
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)
    cv2.rectangle(img, (x_min, y_min - int(1.3 * text_height)), (x_min + text_width, y_min), BOX_COLOR, -1)
    cv2.putText(img, class_name, (x_min, y_min - int(0.3 * text_height)), cv2.FONT_HERSHEY_SIMPLEX, 0.35, TEXT_COLOR,
                lineType=cv2.LINE_AA)
    return img


def visualize(annotations, category_id_to_name):
    img = annotations['image'].copy()
    for idx, bbox in enumerate(annotations['bboxes']):
        img = visualize_bbox(img, bbox, annotations['category_id'][idx], category_id_to_name)
    plt.figure(figsize=(12, 12))
    plt.imshow(img)


limit = 10
counter = 0
for tree in [ann_folder]:

    category_id_to_name = {17: 'cat', 18: 'dog'}
    for file in xmlFiles(tree + '/*.xml'):
        xmlFile = ElementTree.parse(file)
        boxes = xmlFile.findall('object/bndbox')
        bboxes = []
        for box in boxes:
            xmin = box.find('xmin')
            ymin = box.find('ymin')
            xmax = box.find('xmax')
            ymax = box.find('ymax')
            box = [366.7, 80.84, 132.8, 181.84]
            bboxes.append(box)
        img_file = img_folder + "/" + os.path.splitext(os.path.split(file)[1])[0] + ".jpg"
        img = cv2.imread(img_file, 0)
        annotations = {'image': img, 'bboxes': bboxes,
                       'category_id': [18, 17]}

    visualize(annotations, category_id_to_name)
    counter = counter + 1
    if counter > limit:
        break
