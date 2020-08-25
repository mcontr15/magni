#!/usr/bin/env python
#cense removeid for brevity
import rospy
from std_msgs.msg import String
import re
import sys
import os

#cwd = os.getcwd()
#clientsPath = cwd+'/clients'
#print(clientsPath)
#sys.path.insert(1,clientsPath)

from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
from clients.go_home_client import go_home_client
import rosbag

global AMCLFlag

# checkAMCL flag before we can start going home
def checkAMCL(data):
    global AMCLFlag
    if AMCLFlag == False:
        AMCLFlag = True

def goHome(data):
    global AMCLFlag
    print('GUI command:' + str(data) + 'received')
    if AMCLFlag == False:
        print('AMCL not up yet')
    elif AMCLFlag == True and 'home' in str(data):
        print('sending go home!')
        go_home_client()
    else:
        print('GUI command did not include [home]')

def startup():
    global AMCLFlag
    AMCLFlag = False
    rospy.init_node('goHomeListener', anonymous=True)
    #pub = rospy.Publisher('',PoseWithCovarianceStamped, queue_size=10)
    sub = rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped, checkAMCL )
    subLaunch = rospy.Subscriber('launch_cmds',String, goHome )
    # idle around until amcl_pose comes up
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
