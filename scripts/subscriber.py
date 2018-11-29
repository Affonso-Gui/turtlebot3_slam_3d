#!/usr/bin/python

import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray

file = open("log.txt", "w+")
null_pose = Pose()

def callback(msg):
    i = 0
    for pose in msg.poses:
        i += 1
        if pose != null_pose:
            pos = pose.position
            str = 'label {0} \t {1} \t {2} \t {3} \n'.format(i, pos.x, pos.y, pos.z)
            file.write(str)

def listener():
    rospy.init_node('sub_node')
    rospy.Subscriber('/cluster_decomposer/centroid_pose_array', PoseArray, callback)
    rospy.spin()

listener()
