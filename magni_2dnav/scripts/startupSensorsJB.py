#!/usr/bin/env python
#cense removeid for brevity
import rospy
import re
import sys
import os
from nav_msgs.msg import Odometry

global recFlag
# send initial pose once we have from the topic we want

def startSensors(data):
    global recFlag
    if recFlag == False:
        rospy.loginfo('ODOM HAS BEEN RECEIVED, GOOD TO START')
        os.system('roslaunch magni_2dnav magni_configuration_JB.launch')
        recFlag = True

def startup():
    global recFlag
    recFlag = False
    rospy.init_node('startupSensors', anonymous=True)
    sub = rospy.Subscriber('odom',Odometry,startSensors)
    # idle around until we get data from the pointcloud
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
