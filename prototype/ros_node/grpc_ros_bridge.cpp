#include "grpc_ros_bridge.hpp"

GrpcRosBridge::GrpcRosBridge(ros::NodeHandle& nh)
    : nh_(nh),
      move_base_client_("move_base", true) {
    ROS_INFO("Waiting for move_base action server...");
    move_base_client_.waitForServer();
    ROS_INFO("Connected to move_base server");
}

void GrpcRosBridge::processJsonMessage(const std::string& json_str) {
    try {
        auto j = json::parse(json_str);
        
        for (const auto& action : j["actions"]) {
            if (action.contains("navigate")) {
                NavigationAction nav_action{
                    action["navigate"]["name"],
                    action["navigate"]["keywords"].get<std::vector<std::string>>(),
                    action["navigate"]["floor"]
                };
                executeNavigationAction(nav_action);
            }
        }
    } catch (const json::exception& e) {
        ROS_ERROR_STREAM("JSON parsing error: " << e.what());
    }
}

void GrpcRosBridge::executeNavigationAction(const NavigationAction& nav_action) {
    geometry_msgs::PoseStamped target_pose;
    
    if (!getPoseForLocation(nav_action.name, target_pose)) {
        ROS_ERROR_STREAM("Could not find pose for location: " << nav_action.name);
        return;
    }

    move_base_msgs::MoveBaseGoal goal;
    goal.target_pose = target_pose;
    
    ROS_INFO_STREAM("Navigating to: " << nav_action.name);
    move_base_client_.sendGoal(goal);
    

    bool finished = move_base_client_.waitForResult(ros::Duration(300.0));
    
    if (finished) {
        actionlib::SimpleClientGoalState state = move_base_client_.getState();
        ROS_INFO_STREAM("Navigation finished: " << state.toString());
    } else {
        ROS_WARN("Navigation timed out");
        move_base_client_.cancelGoal();
    }
}

bool GrpcRosBridge::getPoseForLocation(
    const std::string& location_name, 
    geometry_msgs::PoseStamped& pose
) {
    // TODO: Implement location lookup
    return false;
}
