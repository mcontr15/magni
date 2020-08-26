#!/usr/bin/env python3
"""trt_yolov3.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLOv3 engine.
"""


import os
import time
import argparse
import sys
import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

from utils.yolov3_classes import get_cls_dict
from utils.yolov3 import TrtYOLOv3
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization

import pyrealsense2 as rs
import numpy as np

import rospy
from std_msgs.msg import Bool

def camera_config(args):
    front_sn = args[1] # johnny_boy front: 017322070445
    ctx = rs.context()
    devices = ctx.query_devices()
    for dev in devices:
        if dev.get_info(rs.camera_info.serial_number) == front_sn:
            dev.hardware_reset()
            print('Resetting Hardware...')        
            rospy.sleep(5)
            break

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(front_sn)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    # Start streaming
    pipeline.start(config)
    return pipeline


def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLOv3 model on Jetson Nano')
    parser = argparse.ArgumentParser(description=desc)
    #parser = add_camera_args(parser)
    parser.add_argument('--model', type=str, default='yolov3-tiny-covid',
                        help='yolov3[-spp|-tiny]-[288|416|608]')
    parser.add_argument('--category_num', type=int, default=5,
                        help='number of object categories [80]')
    parser.add_argument('--front_sn', type=str, default='017322070445',
                        help='Serial number of the front camera')
    args = parser.parse_args()
    return args


def loop_and_detect(pub, pipeline, trt_yolov3, conf_th, vis):
    """Continuously capture images from camera and do object detection.

    # Arguments
      cam: the camera instance (video source).
      trt_yolov3: the TRT YOLOv3 object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
    """
    #full_scrn = False
    fps = 0.0
    tic = time.time()
    people = 4
    people_status = False
    print('Starting detection, listen to topic /people_detection') 
    while True:
        #if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
        #    break
        # Wait for a coherent pair of frames: depth and color
        try:
            frames = pipeline.wait_for_frames()
        # depth_frame = frames.get_depth_frame()
            img = frames.get_color_frame()
            img = np.asanyarray(img.get_data())
            if img is not None:
                boxes, confs, clss = trt_yolov3.detect(img, conf_th)
                if people in clss:
                    people_status = True 
                    pub.publish(people_status)
                elif people not in clss:
                    people_status = False
                    pub.publish(people_status)
        except RuntimeError:
            print('Waiting for frames . . .')

def main():
    model = "yolov3-tiny-covid"
    category_num = 5
    #args = parse_args()

    pub = rospy.Publisher('people_detection', Bool, queue_size=5)
    rospy.init_node('people_detector', anonymous=True)

    pipeline = camera_config(sys.argv)

    cls_dict = get_cls_dict(category_num)
    yolo_dim = model.split('-')[-1]
    if 'x' in yolo_dim:
        dim_split = yolo_dim.split('x')
        if len(dim_split) != 2:
            raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
        w, h = int(dim_split[0]), int(dim_split[1])
    else:
        h = w = int(608)
    if h % 32 != 0 or w % 32 != 0:
        raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)

    trt_yolov3 = TrtYOLOv3(model, (h, w), category_num)

    vis = BBoxVisualization(cls_dict)
    loop_and_detect(pub, pipeline, trt_yolov3, conf_th=0.3, vis=vis)

    pipeline.stop()


if __name__ == '__main__':
    main()
