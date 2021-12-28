#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
import time
from std_srvs.srv import Empty
import numpy as np
import tf
import csv
import time
from datetime import datetime
x=0
y=0
ww=0
rol=0
pitch=0
yaw=0
b=0
t0=0
t1=0,0000001
yawi=0
yaws=0
def poseCallback(pose_message):
    global x , t0
    global y, w ,roll , pitch , yaw , yawi , yaws
    x= pose_message.pose.pose.position.x
    y= pose_message.pose.pose.position.y
    ww = pose_message.pose.pose.orientation
    www=[ww.x,ww.y,ww.z,ww.w]
    ##print(ww)
    #print "pose callback"
    #print ('x = {}'.format(pose_message.x)) #new in python 3
    #print ('y = %f' %pose_message.y) #used in python 2
    #print ('yaw = {}'.format(pose_message.theta)) #new in python 3
    yawi=yaws
    (roll , pitch , yaw)=tf.transformations.euler_from_quaternion(www)
    if yaw<0:
        yaw=yaw+2*math.pi
    t0=time.datetime.now()
    yaws=yaw
    #print t0
    	
    

def go_to(a):

    global yaw
    while(1):
        #print(yaw)
        print(math.atan2(-1,1))

def go_to_goal(x_goal, y_goal):
    global x , t1
    global y, yaw , b , t0 , yaws ,yawi

    velocity_message = Twist()
    cmd_vel_topic='/robot_diff_drive_controller/cmd_vel'
    
    while (True):
        K_linear = 0.5 
        distance = abs(math.sqrt(((x_goal-x) ** 2) + ((y_goal-y) ** 2)))

        linear_speed = distance * K_linear




        deltat=t1-t0
        if ((abs(yaws-yawi)/(delta.second))>1.57):
            yaw=yaw-2*math.pi





        K_angular = 0.5
        desired_angle_goal = math.atan2( y_goal-y,x_goal-x)



        if (desired_angle_goal<=0):
            desired_angle_goal=desired_angle_goal+2*math.pi
        #desired_angle_goal=desired_angle_goal
        
        angular_speed = (desired_angle_goal-yaw)*K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed
        #velocity_message.linear.x = 0
        #velocity_message.angular.z = -5
        velocity_publisher.publish(velocity_message)
        #print(math.pi)
        #print velocity_message.linear.x
        #print velocity_message.angular.z
        #print 'x=', x, 'y=',y ,'yaw',yaw ,'distance' ,distance
#        csvfile = open( 'names'+str(b)+'.csv' , 'r')
#        with csvfile:
#            fieldnames = ['x', 'y', 'yaw' , 'distance' , 'x_goal' , 'y_goal' , 'desired_angle_goal' , 'linear_speed' , 'angular_speed']
#            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            writer.writeheader()
#            writer.writerow([x , y , yaw , distance , x_goal , y_goal , desired_angle_goal , linear_speed , angular_speed])  
        #print(yaw)
        
        t1=time.datetime.now()
        print (yaws,yawi)
        #print (t0,t1)
        if (distance <0.1):
            break





if __name__ == '__main__':
    try:
        
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        #declare velocity publisher
        cmd_vel_topic='/robot_diff_drive_controller/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = "/odom"
        pose_subscriber = rospy.Subscriber(position_topic, Odometry, poseCallback) 
        time.sleep(2)

        #move(1.0, 2.0, False)
        #rotate(30, 90, True)
	#go_to(10)
        go_to_goal(10.0, 0)
        b=b+1

        go_to_goal(10.0, 5.0)
        b=b+1
        go_to_goal(0.0, 5.0)
        b=b+1
        go_to_goal(0.0, 10.0)
        b=b+1
        go_to_goal(10.0, 10.0)
        #setDesiredOrientation(math.radians(90))
       
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
