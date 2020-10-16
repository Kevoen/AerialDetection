
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
            fw.write(str(image_id)+'.tif')
            fw.write(' ')
            fw.write(str(clas))
            fw.write(' ')
            fw.write(str(score))
            fw.write(' ')
            fw.write(str(bboxs[0]))
            fw.write(' ')
            fw.write(str(bboxs[1]))
            fw.write(' ')
            fw.write(str(bboxs[2]))
            fw.write(' ')
            fw.write(str(bboxs[3]))
            fw.write('\n')

if __name__ == "__main__":
    json2txt('C:/Users/HUANG/Downloads/results.pkl.json','C:/Users/HUANG/Downloads/results.txt')