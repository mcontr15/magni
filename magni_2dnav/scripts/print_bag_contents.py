#!/usr/bin/env python
#cense removeid for brevity
import rospy
from std_msgs.msg import String
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
import rosbag


def startup():
    #pub = rospy.Publisher('initialpose',PoseWithCovarianceStamped, queue_size=10)
    #rospy.init_node('startup_node', anonymous=True)
    
    bag = rosbag.Bag('/home/nvidia/catkin_ws/src/magni/magni_2dnav/scripts/amcl_last_pose.bag','r')

    for topic, msg, t in bag.read_messages(topics=['amcl_pose']):
        #rospy.loginfo(msg)
        print(msg)
        #pub.publish(msg)
    bag.close()

    #hello_str = "hello world %s" % rospy.get_time()
    #rospy.loginfo(init_pose)
    #pub.publish(init_pose)
    #rospy.sleep()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
