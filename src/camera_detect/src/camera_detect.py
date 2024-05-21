#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError
import time
from imutils.video import VideoStream
import imutils

class MovementDetectionTurtleBot:
    def __init__(self):
        rospy.init_node('movement_detection_turtlebot', anonymous=True)
        self.bridge = CvBridge()
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.last_movement_time = 0
        self.velocity = Twist()
        self.vs = VideoStream(src=0).start()
        time.sleep(2.0)
        self.fgmask = None

    def detect_movement(self):
        while not rospy.is_shutdown():
            frame = self.vs.read()
            frame = imutils.resize(frame, width=400)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.fgmask is None:
                self.fgmask = gray.copy().astype("float")
                continue

            cv2.accumulateWeighted(gray, self.fgmask, 0.5)
            frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.fgmask))
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

            if np.any(thresh):
                self.last_movement_time = time.time()
                self.stop_turtlebot()
            elif time.time() - self.last_movement_time >= 5:
                self.reset_turtlebot()

            cv2.imshow('Camera Feed', frame)
            cv2.waitKey(1)

    def stop_turtlebot(self):
        self.velocity.linear.x = 0
        self.velocity.angular.z = 0
        self.cmd_vel_pub.publish(self.velocity)

    def reset_turtlebot(self):
        # Set the desired velocity and angular velocity here
        self.velocity.linear.x = 0.2  # Set the linear velocity
        self.velocity.angular.z = 0.5  # Set the angular velocity
        self.cmd_vel_pub.publish(self.velocity)

def main():
    try:
        movement_detection_turtlebot = MovementDetectionTurtleBot()
        movement_detection_turtlebot.detect_movement()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

