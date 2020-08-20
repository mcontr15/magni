#!/usr/bin/env python
import serial
import rospy
import time 
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped
global file_object

def prependLines(text):
	return 'initial_pose_' + text.replace('\n','\ninitial_pose_')

def callback(data):
	global file_object
	#print str(data)
	file_object = open('/home/nvidia/catkin_ws/src/magni_2dnav/param/latest_amcl_pose.yaml','w')
	t = time.localtime()
	current_time = time.strftime("%D-%H:%M:%S",t)
	timeString = str(current_time)
	poseString = str(data)
	#print(poseString)
	#headerString = str(data.header.stamp)
	#poseString = str(data.pose.pose.position)
	#print(timeString)
	print(poseString)
	#file_object.write(headerString)	
	file_object.seek(0,0)
	file_object.write('#')
	file_object.write(timeString)
	file_object.write('\n')
	file_object.write(poseString)
	#file_object.write(prependLines(poseString))
	#file_object.write('\n')
	file_object.close()  

def odom_write():
	global file_object
	print('creating file object')
	#file_object = open('/home/nvidia/catkin_ws/src/magni_2dnav/param/latest_amcl_pose.yaml','w')

	safe_sleep_time = 2.0
	rospy.init_node('amcl_pose_tracking', anonymous=True)
	rospy.sleep(safe_sleep_time)
	rospy.Subscriber("amcl_pose",PoseWithCovarianceStamped,callback)

	# error handle after rospy spin
	rospy.spin()
	print('Keyboard Interrupt Received')
	print('closing AMCL Pose file')
	file_object.close()  

if __name__ == '__main__':   
	odom_write()
		
