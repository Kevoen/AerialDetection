import cv2
import os
import dota_utils as util

def merge_image(srcpath, distrpath):

    imageparent = os.path.join(srcpath, 'images')
    labelparent = os.path.join(srcpath, 'labelTxt')

    imagepath = os.path.join(distrpath, 'images')
    labelpath = os.path.join(distrpath, 'labelTxt')

    for file in os.listdir(imageparent):

        img_path = os.path.join(imageparent, file)

        basename = util.custombasename(file)
        basename = str(int(basename)+2008)
        save_img_path = os.path.join(imagepath, basename + '.tif')
        cv2.imwrite(save_img_path, cv2.imread(img_path))
        print('{} -> {} and save to {}'.format(file, basename, save_img_path))

    for file in os.listdir(labelparent):

        label_path = os.path.join(labelparent, file)

        basename = util.custombasename(file)
        basename = str(int(basename) + 2008)
        save_label_path = os.path.join(labelpath, basename + '.txt')
        txt_save = open(save_label_path, 'w')
        txt = open(label_path, 'r')
        txt_labels = txt.read()
        txt_save.write(txt_labels)
        print('{} -> {} and save to {}'.format(file, basename, save_label_path))




if __name__ == '__main__':
    merge_image('C:/Users/HUANG/Desktop/123/Aerial_dataset', 'C:/Users/HUANG/Desktop/123/Aerial_dataset/2')
    # merge_image('../hk/Aerial_dataset/train', '../hk/Aerial_step1_datasets/train')