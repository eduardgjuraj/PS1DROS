#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

def publish_cmd_vel(linear, angular):
    rospy.init_node('cmd_vel_publisher')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        linear_vel = float(input("Enter linear velocity: "))
        angular_vel = float(input("Enter angular velocity: "))
        publish_cmd_vel(linear_vel, angular_vel)
    except rospy.ROSInterruptException:
        pass
