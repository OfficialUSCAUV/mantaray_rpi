#!/usr/bin/env python3

import rospy
import time
from fsm import fsm
from fsm_basic import fsm_basic
from fsm_pcontrol import fsm_pcontrol
from mantaray_rpi.msg import FloatStamped
from nav_msgs.msg import Odometry
from std_msgs.msg import String, Header
import math

running = True

SUB_NAME = "mantaray"
THRUSTER_COUNT = 8

sub_control_state = fsm()

def thruster_publisher(name, fsm):
    
    rospy.init_node('mantaray_control', anonymous=True) 
    fsm.set_state(1)

    pub = []

    fsm.current_state.set_rot_target(math.radians(0),math.radians(0),math.radians(0))

    for i in range(THRUSTER_COUNT):
        pub.append(rospy.Publisher('/' + name + '/thrusters/'+str(i)+'/input', FloatStamped, queue_size=10))
    

    time_last = time.time()
    while not rospy.is_shutdown():
        fsm.run(100)
        for i in range(THRUSTER_COUNT):
            fs = FloatStamped()
            fs.header.frame_id = 'world'
            fs.header.stamp = rospy.Time.now()
            fs.data = fsm.get_state().get_thrust_list()[i]
            pub[i].publish(fs)

        rate = rospy.Rate(10) # 10hz
        rate.sleep()


def stop():
    print("stop")
    running = False
    rospy.shutdown()



if __name__ == "__main__":
    print("initializing thrusters...")
    time.sleep(8)
    print("thrusters initialized")
    thruster_publisher(SUB_NAME, sub_control_state)
