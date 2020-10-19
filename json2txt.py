
# {"image_id": 1, "bbox": [, , , ], "score": 0.05416450276970863, "category_id": 2}

import json
import os
import codecs

def json2txt(path_json,path_save_txt):
    Json = json.load(codecs.open(path_json, 'r', 'utf-8-sig'))
    with open(path_save_txt,'a') as fw:

        for obj in Json:
            image_id = obj['image_id']
            bboxs = obj['bbox']
            score = obj['score']
            clas = obj['category_id']
            x1 = int(bboxs[0])
            y1 = int(bboxs[1])
            x2 = int(bboxs[2])
            y2 = int(bboxs[3])
            fw.write(str(image_id)+'.tif')
            fw.write(' ')
            fw.write(str(clas))
            fw.write(' ')
            fw.write(str(score).split(".")[0] + "." + str(score).split(".")[1][:2])
            fw.write(' ')
            fw.write(str(x1))
            fw.write(' ')
            fw.write(str(y1))
            fw.write(' ')
            fw.write(str(x2))
            fw.write(' ')
            fw.write(str(y2))
            fw.write('\n')

if __name__ == "__main__":
    json2txt('C:/Users/HUANG/Downloads/results.pkl (2).json','C:/Users/HUANG/Downloads/results.txt')
    #json2txt('/AerialDetection/work_dirs/faster_rcnn_r50_fpn_1x_aerial/results.pkl.json','/AerialDetection/work_dirs/faster_rcnn_r50_fpn_1x_aerial/results.txt')