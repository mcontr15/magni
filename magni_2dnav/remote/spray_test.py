#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
 
def talker():
	pub = rospy.Publisher('spray_testing', String, queue_size=10)
     	rospy.init_node('spray_testing', anonymous=True)
     	rate = rospy.Rate(10) # 10hz
     	while not rospy.is_shutdown():
        	hello_str = "hello world " + str(2) + ' '
        	rospy.loginfo(hello_str)
        	pub.publish(hello_str)
        	rate.sleep()
 
if __name__ == '__main__':
	try:
        	talker()
     	except rospy.ROSInterruptException:
        	pass
