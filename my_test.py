from mmdet.apis import init_detector, inference_detector, show_result, draw_poly_detections
import mmcv
from mmcv import Config
from mmdet.datasets import get_dataset
import cv2
import os
import numpy as np
from tqdm import tqdm
import DOTA_devkit.polyiou as polyiou
import math
import pdb


def py_cpu_nms_poly_fast_np(dets, thresh):
    obbs = dets[:, 0:-1]
    x1 = np.min(obbs[:, 0::2], axis=1)
    y1 = np.min(obbs[:, 1::2], axis=1)
    x2 = np.max(obbs[:, 0::2], axis=1)
    y2 = np.max(obbs[:, 1::2], axis=1)
    scores = dets[:, 8]
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    polys = []
    for i in range(len(dets)):
        tm_polygon = polyiou.VectorDouble([dets[i][0], dets[i][1],
                                            dets[i][2], dets[i][3],
                                            dets[i][4], dets[i][5],
                                            dets[i][6], dets[i][7]])
        polys.append(tm_polygon)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        ovr = []
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        hbb_inter = w * h
        hbb_ovr = hbb_inter / (areas[i] + areas[order[1:]] - hbb_inter)
        h_inds = np.where(hbb_ovr > 0)[0]
        tmp_order = order[h_inds + 1]
        for j in range(tmp_order.size):
            iou = polyiou.iou_poly(polys[i], polys[tmp_order[j]])
            hbb_ovr[h_inds[j]] = iou

        try:
            if math.isnan(ovr[0]):
                pdb.set_trace()
        except:
            pass
        inds = np.where(hbb_ovr <= thresh)[0]
        order = order[inds + 1]
    return keep

class DetectorModel():
    def __init__(self,
                 config_file,
                 checkpoint_file):
        # init RoITransformer
        self.config_file = config_file
        self.checkpoint_file = checkpoint_file
        self.cfg = Config.fromfile(self.config_file)
        self.data_test = self.cfg.data['test']
        self.dataset = get_dataset(self.data_test)
        self.classnames = self.dataset.CLASSES
        self.model = init_detector(config_file, checkpoint_file, device='cuda:0')

    def inference_single(self, imagname, slide_size, chip_size):
        img = mmcv.imread(imagname)
        height, width, channel = img.shape
        slide_h, slide_w = slide_size
        hn, wn = chip_size
        # TODO: check the corner case
        # import pdb; pdb.set_trace()
        total_detections = [np.zeros((0, 9)) for _ in range(len(self.classnames))]

        for i in tqdm(range(int(width / slide_w + 1))):
            for j in range(int(height / slide_h) + 1):
                subimg = np.zeros((hn, wn, channel))
                # print('i: ', i, 'j: ', j)
                chip = img[j*slide_h:j*slide_h + hn, i*slide_w:i*slide_w + wn, :3]
                subimg[:chip.shape[0], :chip.shape[1], :] = chip

                chip_detections = inference_detector(self.model, subimg)

                # print('result: ', result)
                for cls_id, name in enumerate(self.classnames):
                    chip_detections[cls_id][:, :8][:, ::2] = chip_detections[cls_id][:, :8][:, ::2] + i * slide_w
                    chip_detections[cls_id][:, :8][:, 1::2] = chip_detections[cls_id][:, :8][:, 1::2] + j * slide_h
                    # import pdb;pdb.set_trace()
                    try:
                        total_detections[cls_id] = np.concatenate((total_detections[cls_id], chip_detections[cls_id]))
                    except:
                        import pdb; pdb.set_trace()
        # nms
        for i in range(len(self.classnames)):
            keep = py_cpu_nms_poly_fast_np(total_detections[i], 0.1)
            total_detections[i] = total_detections[i][keep]
        return total_detections
    def inference_single_vis(self, srcpath, dstpath, slide_size, chip_size):
        detections = self.inference_single(srcpath, slide_size, chip_size)
        img = draw_poly_detections(srcpath, detections, self.classnames, scale=1, threshold=0.3)
        cv2.imwrite(dstpath, img)

    def inference_multiple_vis(self, srcpath, dstpath, imgpath, slide_size, chip_size):
        import pdb
        import random
        scale = 1
        threshold = 0.3
        class_names = self.classnames
        color_white = (255, 255, 255)
        assert isinstance(class_names, (tuple, list))
        src_img_path = srcpath
        text_path = dstpath + '科目四_NCHU_ODT01.txt'
        txt = open(text_path, 'w')
        for file in os.listdir(src_img_path):
            img_path = os.path.join(src_img_path, file)
            detections = self.inference_single(img_path, slide_size, chip_size)
            img = mmcv.imread(img_path)
            for j, name in enumerate(class_names):
                try:
                    dets = detections[j]
                except:
                    pdb.set_trace()
                for det in dets:
                    bbox = det[:8] * scale
                    score = det[-1]
                    if score < threshold:
                        continue
                    bbox = list(map(int, bbox))
                    txt.write(str(file))
                    txt.write(' ')
                    txt.write(str(class_names[j]))
                    txt.write(' ')
                    txt.write(str(score).split(".")[0] + "." + str(score).split(".")[1][:2])
                    txt.write(' ')
                    txt.write(str(int(bbox[0])))
                    txt.write(' ')
                    txt.write(str(int(bbox[1])))
                    txt.write(' ')
                    txt.write(str(int(bbox[2])))
                    txt.write(' ')
                    txt.write(str(int(bbox[3])))
                    txt.write(' ')
                    txt.write(str(int(bbox[4])))
                    txt.write(' ')
                    txt.write(str(int(bbox[5])))
                    txt.write(' ')
                    txt.write(str(int(bbox[6])))
                    txt.write(' ')
                    txt.write(str(int(bbox[7])))
                    txt.write(' ')
                    txt.write('\n')

                    print("label wrote: ", file)

                    color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
                    cv2.circle(img, (bbox[0], bbox[1]), 3, (0, 0, 255), -1)
                    for i in range(3):
                        cv2.line(img, (bbox[i * 2], bbox[i * 2 + 1]), (bbox[(i + 1) * 2], bbox[(i + 1) * 2 + 1]),
                                 color=color, thickness=2)
                    cv2.line(img, (bbox[6], bbox[7]), (bbox[0], bbox[1]), color=color, thickness=2)
                    cv2.putText(img, '%s %.3f' % (class_names[j], score), (bbox[0], bbox[1] + 10),
                                color=color_white, fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5)
            cv2.imwrite(os.path.join(imgpath, file), img)
            print("images wrote: ", os.path.join(imgpath, file))

if __name__ == '__main__':
    # roitransformer = DetectorModel(r'configs/Aerial/faster_rcnn_RoITrans_r50_fpn_1x_dota.py',
    #               r'work_dirs/faster_rcnn_RoITrans_r50_fpn_1x_dota/epoch_12.pth')
    roitransformer = DetectorModel(r'configs/Aerial/faster_rcnn_RoITrans_r50_fpn_1x_aerial.py',
                                   r'work_dirs/epoch_12.pth')

    # roitransformer.inference_single_vis(r'/hk/Aerial_step1_datasets/test/images/1.tif',
    #                                    r'1_out.tif',
    #                                     (512, 512),
    #                                    (1024, 1024))
    roitransformer.inference_multiple_vis(r'/hk/Aerial_step1_datasets/test/images', r'./', r'./output',(512, 512), (1024, 1024))

