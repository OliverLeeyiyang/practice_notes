#!/usr/bin/env python
#coding=utf-8

import roslib
import rospy
from gazebo_msgs.msg import ModelStates
# Set_model_state 该话题用的是ModelState类型的话题
from gazebo_msgs.msg import ModelState
from std_msgs.msg import Float64

TOPIC_TO_SET = '/gazebo/set_model_state'


class RPControl():
    def __init__(self):
        rospy.init_node('row_pitch_control')
        nodename = rospy.get_name()
        rospy.loginfo("%s started" % nodename)

        rospy.Subscriber('gazebo/model_states', ModelStates, self.twistCallback)
        self.pub_set = rospy.Publisher(TOPIC_TO_SET, ModelState, queue_size=10)

        self.rate = rospy.get_param("~rate", 10)
        self.timeout_ticks = rospy.get_param("~timeout_ticks", 2)
        self.ticks_since_target = 0

        self.x = 0.0
        self.y = 0.0
        self.model_states = ModelState()
        self.model_states.model_name = 'pudong'
        self.model_states.reference_frame = 'world'

    def spin(self):
        r = rospy.Rate(self.rate)
        idle = rospy.Rate(10)
        then = rospy.Time.now()
        self.ticks_since_target = self.timeout_ticks

        ###### main loop  ######
        while not rospy.is_shutdown():

            while not rospy.is_shutdown() and self.ticks_since_target < self.timeout_ticks:
                self.spinOnce()
                r.sleep()
            idle.sleep()

    def spinOnce(self):
        self.ticks_since_target += 1

        if self.x != 0.0 or self.y != 0.0:
            self.model_states.pose.orientation.x = 0.0
            self.model_states.pose.orientation.y = 0.0
            self.pub_set.publish(self.model_states)

    def twistCallback(self, msg):
        self.ticks_since_target = 0

        self.model_states.pose = msg.pose[-1]
        self.model_states.twist = msg.twist[-1]
        self.x = msg.pose[-1].orientation.x
        self.y = msg.pose[-1].orientation.y


if __name__ == '__main__':
    rpc = RPControl()
    rpc.spin()
