from PIL import Image,ImageDraw
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv

image_path = 'D:/迅雷下载/Aerial_step1_datasets/test/images/60.tif'
# image_path = 'D:/迅雷下载/Aerial_step1_datasets/train/images/1.tif'
image = Image.open(image_path)
#创建一个可以在给定图像上绘图的对象
draw = ImageDraw.Draw(image)

#draw.polygon([(902,1217),(1288,1215),(1288,1269),(903,1271)], outline=(255,0,0))
#坐标参数依次是左上角、右上角、右下角、左下角，outline里面是RGB参数：红、绿、蓝
# draw.polygon([(451,95),(153,39),(749,95),(451,451)], outline=(255,0,0))
# draw.rectangle([280, 112, 293, 462], outline=(255,0,0))
# draw.rectangle([634,114,106,30], outline=(255,0,0))
# draw.rectangle([457,93,140,42], outline=(255,0,0))
# draw.polygon([789, 300, 183, 372, 1395, 300, 789, 372], outline=(255,0,0))

draw.polygon([945, 220, 933, 193, 1018, 156, 1030, 183 ], outline=(255,0,0))
# draw.polygon([893, 133, 891, 156, 784, 149, 786, 126 ], outline=(255,0,0))
# draw.polygon([600, 106, 598, 135, 442, 126, 443, 97 ], outline=(255,0,0))
image.show()