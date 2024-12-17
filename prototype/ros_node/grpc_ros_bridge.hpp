#pragma once
#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include "action_types.hpp"
#include <nlohmann/json.hpp>
using json = nlohmann::json;

class GrpcRosBridge {
public:
    GrpcRosBridge(ros::NodeHandle& nh);
    void processJsonMessage(const std::string& json_str);

private:
    void executeNavigationAction(const NavigationAction& nav_action);
    bool getPoseForLocation(const std::string& location_name, geometry_msgs::PoseStamped& pose);
    
    ros::NodeHandle& nh_;
    actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> move_base_client_;
    // Add any additional members needed for location management
};
