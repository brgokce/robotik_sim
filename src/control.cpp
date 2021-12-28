
#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "nav_msgs/Odometry.h"
#include <sstream>
#include <math.h>
using namespace std;

ros::Publisher velocity_publisher;
ros::Subscriber pose_subscriber;
double anlik_x, anlik_y, anlik_w;



const double x_min = 0.0;
const double y_min = 0.0;
const double x_max = 11.0;
const double y_max = 11.0;

const double PI = 3.14159265359;



void poseCallback(const nav_msgs::Odometry::ConstPtr & msg);
void moveGoal(nav_msgs::Odometry goal_pose, double distance_tolerance);
nav_msgs::Odometry goalpose;

int main(int argc, char **argv)
{
	// Initiate new ROS node named "talker"
	ros::init(argc, argv, "robotik");
	ros::NodeHandle n;
	double speed, angular_speed;
	double distance, angle;
	bool isForward, clockwise;
	float a,b,w;

	
	velocity_publisher = n.advertise<geometry_msgs::Twist>("/robot_diff_drive_controller/cmd_vel", 10);
	pose_subscriber = n.subscribe("/odom", 10, poseCallback);


	ros::Rate loop(0.5);
	
	
	goalpose.pose.pose.position.x=0;
	goalpose.pose.pose.position.y=10;
	goalpose.pose.pose.orientation.w=0;
	moveGoal(goalpose, 1);

/*	pose.pose.pose.position.x=-6;
	pose.pose.pose.position.y=-6;
	pose.pose.pose.orientation.w=0;
	moveGoal(pose, 0.01); 
*/

	loop.sleep();

	ros::spin();

	return 0;
}

void poseCallback(const nav_msgs::Odometry::ConstPtr & msg){

     anlik_x = msg->pose.pose.position.x ;
     anlik_y = msg->pose.pose.position.y ;
     anlik_w = msg->pose.pose.orientation.w ;
anlik_x=(round(anlik_x*100))/100;
anlik_y=(round(anlik_y*100))/100;
anlik_w=(round(anlik_w*100))/100;
cout<<("deger")<<endl; 
cout<<("%f",anlik_x)<<endl; 
cout<<("%f",anlik_y)<<endl; 
cout<<("%f",anlik_w)<<endl;


}



double getDistance(double x1, double y1, double x2, double y2){
	return sqrt(pow((x2-x1),2)+pow((y2-y1),2));
}


void moveGoal(nav_msgs::Odometry  goal_pose, double distance_tolerance){

	geometry_msgs::Twist vel_msg;

	ros::Rate loop_rate(100);
	double E = 0.0;
	do{
		/****** Proportional Controller ******/
		//linear velocity in the x-axis
		double Kp=1.0;
		double Ki=0.02;
		//double v0 = 2.0;
		//double alpha = 0.5;
		//double e = getDistance(anlik_x, anlik_y, goal_pose.pose.pose.position.x, goal_pose.pose.pose.position.y);
		//double E = E+e;
		//Kp = v0 * (exp(-alpha)*error*error)/(error*error);
		vel_msg.linear.x = (Kp*getDistance(anlik_x, anlik_y, goal_pose.pose.pose.position.x, goal_pose.pose.pose.position.y));
		vel_msg.linear.y =0;
		vel_msg.linear.z =0;
		//angular velocity in the z-axis
		vel_msg.angular.x = 0;
		vel_msg.angular.y = 0;
		vel_msg.angular.z = 4*((atan2 (goal_pose.pose.pose.position.y - anlik_y, goal_pose.pose.pose.position.x - anlik_x))-anlik_w );

		velocity_publisher.publish(vel_msg);

		ros::spinOnce();
		loop_rate.sleep();

	}while(getDistance(-anlik_x, anlik_y, goal_pose.pose.pose.position.x, goal_pose.pose.pose.position.y)>distance_tolerance);
	cout<<"end move goal"<<endl;
	vel_msg.linear.x =0;
	vel_msg.angular.z = 0;
	velocity_publisher.publish(vel_msg);
}



















































