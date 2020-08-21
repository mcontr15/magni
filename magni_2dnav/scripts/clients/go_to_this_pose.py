#! /usr/bin/env python

# uses the move base actionlib service
# call this client to go home

from __future__ import print_function
import sys
import rospy
# Brings in the SimpleActionClient
import actionlib
# Brings in the messages used by the fibonacci action, including the
# goal message and the result message.
import magni_2dnav.msg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def go_to_this_pose_client(posx,posy,posz,ox,oy,oz,ow):
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    #client = actionlib.SimpleActionClient('go_to_this_pose', actionlib_tutorials.msg.GoToTargetPoseAction)
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    # Waits until the action server has started up and started
    # listening for goals.
    # print('wating for server to be started')
    client.wait_for_server()

    #print('creating goal')
    # Creates a goal to send to the action server.
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = posx
    goal.target_pose.pose.position.y = posy
    goal.target_pose.pose.position.z = posz
    goal.target_pose.pose.orientation.x = ox
    goal.target_pose.pose.orientation.y = oy
    goal.target_pose.pose.orientation.z = oz
    goal.target_pose.pose.orientation.w = ow
    #print('sending goal')

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

        if len(sys.argv) == 8:
            posx = float(sys.argv[1])
            posy = float(sys.argv[2])
            posz = float(sys.argv[3])
            ox = float(sys.argv[4])
            oy = float(sys.argv[5])
            oz = float(sys.argv[6])
            ow = float(sys.argv[7])
        else:
            print('Usage Error: provide position and orientation arguments')
            sys.exit(1)

        # nominal execution
        rospy.init_node('go_to_this_pose_client_py')
        result = go_to_this_pose_client(posx,posy,posz,ox,oy,oz,ow)

        if result:
            rospy.loginfo('We went to target pose!')
    except rospy.ROSInterruptException:
        rospy.loginfo("program interrupted before completion")
