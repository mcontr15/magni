#!/usr/bin/env python
#cense removeid for brevity
import rospy
import re
import sys
import os
from sensor_msgs.msg import PointCloud2

global recFlag
# send initial pose once we have from the topic we want

def startMoveBase():
    global recFlag

    if recFlag == False:
        #os.system('roslaunch magni_2dnav teb_.launch')
        print('VOXEL GRID HAS BEEN RECEIVED, GOOD TO START')
        os.system('roslaunch magni_2dnav teb_move_base.launch')
        recFlag = True

def startup():
    global recFlag
    recFlag = False
    rospy.init_node('startupMoveBase', anonymous=True)
    sub = rospy.Subscriber('voxel_grid/output',PointCloud2, startMoveBase() )
    # idle around until we get data from the pointcloud
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
