#include <ros/ros.h>
#include "grpc_ros_bridge.hpp"
#include <grpcpp/grpcpp.h>
// Include generated gRPC headers

int main(int argc, char** argv) {
    ros::init(argc, argv, "grpc_navigation_node");
    ros::NodeHandle nh;
    
    GrpcRosBridge bridge(nh);

    std::string server_address("0.0.0.0:50051");
    // TODO: gRPC service implementation
    
    ros::spin();
    return 0;
}
