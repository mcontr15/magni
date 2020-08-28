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
global sub
# send initial pose once we an initial Pose have from the topic we want

def sendInitialPose(data):
    global pub
    global sentFlag
    global sub
    print(str(sentFlag))
    if sentFlag == False:
        bag = rosbag.Bag('/home/nvidia/catkin_ws/src/magni/magni_2dnav/scripts/amcl_last_pose.bag','r')
        bag.reindex()
        for topic, msg, t in bag.read_messages(topics=['amcl_pose']):
            print('sent last location known')
            rospy.loginfo('publishing last bag message: ')
            rospy.loginfo(msg)
            pub.publish(msg)
        bag.close()
        sentFlag = True
        sub.unregister()

def startup():
    global sentFlag
    global pub
    global sub
    sentFlag = False
    rospy.init_node('startupPoseTracking', anonymous=True)
    rospy.sleep(2.0)
    pub = rospy.Publisher('initialpose',PoseWithCovarianceStamped, queue_size=10)
    sub = rospy.Subscriber('amcl_pose',PoseWithCovarianceStamped, sendInitialPose )
    # idle around until amcl_pose comes up
    rospy.spin()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
