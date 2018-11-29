# https://www.robotech-note.com/entry/2018/04/15/221524

import rospy
from visualization_msgs.msg import Marker, MarkerArray

rospy.init_node("marker_pub")

pub = rospy.Publisher("map_spots", MarkerArray, queue_size = 10)
rate = rospy.Rate(10)

id=0

def make_marker(name, x, y, z):
    marker = Marker()
    marker.header.frame_id = "map"
    marker.header.stamp = rospy.Time.now()

    global id
    marker.ns = "basic_shapes"
    marker.id = id
    id+=1

    marker.action = Marker.ADD

    marker.text = name

    marker.pose.position.x = x
    marker.pose.position.y = y
    marker.pose.position.z = z+0.3

    marker.color.r = 1.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.color.a = 1.0

    marker.lifetime = rospy.Duration()

    marker.scale.z = 0.3
    marker.type = 9 # text

    return marker

with open("result.txt", "r") as input:
    marker_array = []
    for line in input:
        arg_list = line.split('\t')
        marker = make_marker(arg_list[0].strip(), *map(float, arg_list[1:]))
        marker_array.append(marker)

msg = MarkerArray(marker_array)

while not rospy.is_shutdown():
    pub.publish(msg)
    rate.sleep()
