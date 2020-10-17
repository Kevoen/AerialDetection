import dota_utils as util
import os
import cv2
import json
from PIL import Image

import sys
import codecs
import numpy as np
import re
import math
import shapely.geometry as shgeo

wordname_6 = ['1', '2', '3', '3', '4', '5','6']


def parse_aerial_poly2(filename):
    objects = parse_aerial_poly(filename)
    for obj in objects:
        obj['poly'] = util.TuplePoly2Poly(obj['poly'])
        obj['poly'] = list(map(int, obj['poly']))
    return objects

def Aerial2COCOTrain(srcpath, destfile, cls_names):

    imageparent = os.path.join(srcpath, 'images')
    labelparent = os.path.join(srcpath, 'labelTxt')

    data_dict = {}
    data_dict['images'] = []
    data_dict['categories'] = []
    data_dict['annotations'] = []

    for idex, name in enumerate(cls_names):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    inst_count = 1
    image_id = 1

    with open(destfile, 'w') as f_out:
        filenames = util.GetFileFromThisRootDir(labelparent)
        for file in filenames:
            basename = util.custombasename(file)

            imagepath = os.path.join(imageparent, basename + '.tif')

            img = cv2.imread(imagepath)
            height, width, c = img.shape

            single_image = {}
            single_image['file_name'] = basename + '.tif'
            single_image['id'] = image_id
            single_image['width'] = width
            single_image['height'] = height
            data_dict['images'].append(single_image)

            # annotations
            objects = parse_aerial_poly2(file)
            for obj in objects:
                single_obj = {}
                single_obj['area'] = obj['area']
                single_obj['category_id'] = cls_names.index(obj['name']) + 1
                single_obj['segmentation'] = []
                single_obj['segmentation'].append(obj['poly'])
                single_obj['iscrowd'] = 0
                xmin, ymin, xmax, ymax = min(obj['poly'][0::2]), min(obj['poly'][1::2]), \
                                         max(obj['poly'][0::2]), max(obj['poly'][1::2])

                width, height = xmax - xmin, ymax - ymin
                single_obj['bbox'] = xmin, ymin, width, height
                single_obj['image_id'] = image_id
                data_dict['annotations'].append(single_obj)
                single_obj['id'] = inst_count
                inst_count = inst_count + 1
            image_id = image_id + 1
        json.dump(data_dict, f_out, indent=2)

def Aerial2COCOTest(srcpath, destfile, cls_names):

    imageparent = os.path.join(srcpath, 'images')
    data_dict = {}

    data_dict['images'] = []
    data_dict['categories'] = []
    for idex, name in enumerate(cls_names):
        single_cat = {'id': idex + 1, 'name': name, 'supercategory': name}
        data_dict['categories'].append(single_cat)

    image_id = 1
    with open(destfile, 'w') as f_out:
        filenames = util.GetFileFromThisRootDir(imageparent)
        for file in filenames:
            basename = util.custombasename(file)
            imagepath = os.path.join(imageparent, basename + '.tif')
            img = Image.open(imagepath)
            height = img.height
            width = img.width

            single_image = {}
            single_image['file_name'] = basename + '.tif'
            single_image['id'] = image_id
            single_image['width'] = width
            single_image['height'] = height
            data_dict['images'].append(single_image)

            image_id = image_id + 1
        json.dump(data_dict, f_out, indent=2)


def parse_aerial_poly(filename):
    """
        parse the aerial dataset ground truth in the format:
        [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    """
    objects = []

    f = []
    if (sys.version_info >= (3, 5)):
        fd = open(filename, 'r')
        f = fd
    elif (sys.version_info >= 2.7):
        fd = codecs.open(filename, 'r')
        f = fd

    while True:
        line = f.readline()

        if line:
            splitlines = line.strip().split(' ')
            object_struct = {}
            if (len(splitlines) < 9):
                continue
            if (len(splitlines) >= 9):
                object_struct['name'] = splitlines[0]

            object_struct['poly']= [
                (float(splitlines[1]),float(splitlines[2])),
                (float(splitlines[3]),float(splitlines[4])),
                (float(splitlines[5]),float(splitlines[6])),
                (float(splitlines[7]),float(splitlines[8]))
             ]
            gtpoly = shgeo.Polygon(object_struct['poly']) #矩形框
            object_struct['area'] = gtpoly.area     #返回面积

            objects.append(object_struct) #返回gt里的标记BBox
        else:
            break
    return objects



if __name__ == "__main__":
    Aerial2COCOTrain(r'/hk/Aerial_step1_datasets/train', r'/hk/Aerial_step1_datasets/train/Aerial_step1_dataset.json', wordname_6)
    Aerial2COCOTest(r'/hk/Aerial_step1_datasets/test', r'/hk/Aerial_step1_datasets/test/Aerial_step1_dataset.json', wordname_6)
