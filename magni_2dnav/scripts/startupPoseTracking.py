#!/usr/bin/env python
#cense removeid for brevity
import rospy
from std_msgs.msg import String
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
import rosbag

global sentFlag
global pub

# send initial pose once we have from the topic we want

def sendInitialPose(data):
    global pub
    global sentFlag
    if sentFlag == False:
        bag = rosbag.Bag('amcl_last_pose.bag','r')
        for topic, msg, t in bag.read_messages(topics=['amcl_pose']):
            rospy.loginfo(msg)
            pub.publish(msg)
        bag.close()
        sentFlag = True

def startup():
    global sentFlag
    global pub
    sentFlag = False
    rospy.init_node('startupPoseTracking', anonymous=True)
    pub = rospy.Publisher('initialpose',PoseWithCovarianceStamped, queue_size=10)
    sub = rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped, sendInitialPose )

    # idle around until amcl_pose comes up
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
