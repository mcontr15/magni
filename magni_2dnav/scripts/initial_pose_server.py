#!/usr/bin/env python
#!/usr/bin/env python

from __future__ import print_function

from magni_2dnav.srv import *
import rospy
import time 
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped

global pub

def handle_initial_pose(req):
    global pub
    print("Got the initial pose: " + str(req))
    pub.publish(req)
    print("published to the topic")
    
def initial_pose_server():
    global pub
    rospy.init_node('initial_pose_server')
    pub = rospy.Publisher('initialpose',String, queue_size=10)
    s = rospy.Service('initial_pose',InitialPose,handle_initial_pose)
    print("Ready to send initial_pose.")
    rospy.spin()

if __name__ == "__main__":
    initial_pose_server()
