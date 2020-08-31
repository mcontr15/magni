#!/usr/bin/env python

import rospy
import re
import sys
import os
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped

global recFlag
# start GUI once AMCL pose is ready
def startSensors(data):
    global recFlag
    if recFlag == False:

        print('ALL SENSORS HAVE BEEN ACTIVATED ON THE ROBOT, ACTIVATING GUI')
        os.system('rosrun magni_2dnav GUI_2.py')
        recFlag = True

def startup():
    global recFlag
    recFlag = False
    rospy.init_node('startupGUI2', anonymous=True)
    sub = rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped,startSensors)
    # idle around until we get data from the pointcloud
    print('waiting for amcl topic')

    rospy.spin()


if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
