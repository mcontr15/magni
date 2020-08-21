#! /usr/bin/env python

# uses the move base actionlib service
# call this client to go home

from __future__ import print_function

import rospy
# Brings in the SimpleActionClient
import actionlib
# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import magni_2dnav.msg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def go_home_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    #client = actionlib.SimpleActionClient('go_home', actionlib_tutorials.msg.GoHomeAction)
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    # Waits until the action server has started up and started
    # listening for goals.
    print('wating for server to be started')
    client.wait_for_server()
    print('creating goal')
    # Creates a goal to send to the action server.
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 7.331
    goal.target_pose.pose.position.y = -0.694
    goal.target_pose.pose.position.z = 0.0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.549
    goal.target_pose.pose.orientation.w = 0.836
    print('sending goal')

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('go_home_client_py')
        result = go_home_client()
        if result:
            rospy.loginfo('We went home!')
    except rospy.ROSInterruptException:
        rospy.loginfo("program interrupted before completion")
