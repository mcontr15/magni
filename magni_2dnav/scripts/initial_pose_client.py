#!/usr/bin/env python

from __future__ import print_function
import sys
import rospy
from magni_2dnav.srv import *
import time 
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped

def send_initial_pose_once(path):
    pass

def initial_pose_client(path):
    rospy.wait_for_service('initial_pose')
    try:
        initial_pose = rospy.ServiceProxy('initial_pose',InitialPose)
        resp1 = initial_pose(path)
        #return resp1.sum
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [file_path including poseWithCovarianceStamped]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = (str(sys.argv[1]))
    elif len(sys.argv) == 1:
        path = '/home/nvidia/catkin_ws/src/magni_2dnav/param/latest_amcl_pose.yaml'
    else:
        print(usage())
        sys.exit(1)
    print("Requesting Pose Msg With: %s"%(path))
