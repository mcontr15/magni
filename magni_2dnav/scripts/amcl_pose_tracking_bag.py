#!/usr/bin/env python
import serial
import rospy
import time 
import re
import rosbag
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
global bag

def callback(data):
	global bag
        bag = rosbag.Bag('/home/nvidia/catkin_ws/src/magni/magni_2dnav/scripts/amcl_last_pose.bag','w')
        rospy.loginfo(data)
        bag.write('amcl_pose',data)
	bag.close() 

def bag_write():
        global bag
	print('creating bag file')
	safe_sleep_time = 1.0
	rospy.init_node('amcl_pose_tracking', anonymous=True)
	rospy.sleep(safe_sleep_time)
	rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,callback)
        print('lets go for a spin!')
	# error handle after rospy spin
	rospy.spin()
	print('Keyboard Interrupt Received')
	print('closing AMCL Pose file')
	bag.close()  

if __name__ == '__main__':
        # sleep for a bit before writing anything to the file
	bag_write()
		
