from PIL import Image,ImageDraw
import numpy as np

# image_path = 'D:/迅雷下载/Aerial_step1_datasets/test/images/1.tif'
image_path = 'D:/迅雷下载/Aerial_step1_datasets/train/images/1.tif'
image = Image.open(image_path)
#创建一个可以在给定图像上绘图的对象
draw = ImageDraw.Draw(image)

#draw.polygon([(902,1217),(1288,1215),(1288,1269),(903,1271)], outline=(255,0,0))
#坐标参数依次是左上角、右上角、右下角、左下角，outline里面是RGB参数：红、绿、蓝
# draw.polygon([(451,95),(153,39),(749,95),(451,451)], outline=(255,0,0))
# draw.rectangle([785,124,113,33], outline=(255,0,0))
# draw.rectangle([634,114,106,30], outline=(255,0,0))
# draw.rectangle([457,93,140,42], outline=(255,0,0))
draw.polygon([586, 459, 577,441, 646, 410, 654, 428], outline=(255,0,0))
draw.polygon([559, 422, 627, 395, 635, 414, 566, 441], outline=(255,0,0))
image.show()