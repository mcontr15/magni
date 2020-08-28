#!/usr/bin/env python
#cense removeid for brevity
import rospy
import re
import sys
import os
from sensor_msgs.msg import PointCloud2

global recFlag
global frontFlag
# send initial pose once we have from the topic we want

def initFrontFlag(data):
    global recFlag
    global frontFlag
    frontFlag = True
    #print('in the front flag: ' + str(recFlag) + ' ' + str(frontFlag))

def startMoveBase(data):
    global recFlag
    global frontFlag
    #print(str('in moveBase: ' + str(recFlag) + ' ' + str(frontFlag)))
    if recFlag == False and frontFlag:
        #os.system('roslaunch magni_2dnav teb_.launch')
        print('voxel grid recevied, good to start')
        rospy.loginfo('VOXEL GRIDS HAS BEEN RECEIVED, GOOD TO START')
        os.system('roslaunch magni_2dnav teb_move_base.launch')
        recFlag = True

def startup():
    global recFlag
    global frontFlag
    recFlag = False
    frontFlag = False
    rospy.init_node('startupMoveBase', anonymous=True)
    sub = rospy.Subscriber('voxel_grid_back/output',PointCloud2, startMoveBase )
    subFront = rospy.Subscriber('voxel_grid_front/output',PointCloud2, initFrontFlag )
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
