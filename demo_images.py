from mmdet.apis import init_detector, inference_detector, show_result
import mmcv

config_file = 'configs/Aerial/faster_rcnn_r50_fpn_1x_aerial.py'
checkpoint_file = 'work_dirs/faster_rcnn_r50_fpn_1x_aerial/epoch_12.pth'
imgdir = '/hk/Aerial_dataset/test/images/100001422.bmp'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')

# test a single image and show the results
# img = 'test.jpg'  # or img = mmcv.imread(img), which will only load it once
img = mmcv.imread(imgdir)
result = inference_detector(model, img)
# visualize the results in a new window
show_result(img, result, model.CLASSES)
# or save the visualization results to image files
show_result(img, result, model.CLASSES, out_file='result.jpg')

# test a video and show the results
# video = mmcv.VideoReader('video.mp4')
# for frame in video:
#     result = inference_detector(model, frame)
#     show_result(frame, result, model.CLASSES, wait_time=1)