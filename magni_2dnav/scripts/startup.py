#cense removeid for brevity
import rospy
from std_msgs.msg import String
import re
from std_msgs.msg import String
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import PoseWithCovarianceStamped

def extractPoseMessage:
    initialPose = PoseWithCovarianceStamped()
    file_object = open('/home/nvidia/catkin_ws/src/magni_2dnav/param/latest_amcl_pose.yaml','w')


def startup():



    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    #rate = rospy.Rate(10) # 10hz
    #while not rospy.is_shutdown():
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    #rospy.sleep()

if __name__ == '__main__':
    try:
        startup()
    except rospy.ROSInterruptException:
        pass
