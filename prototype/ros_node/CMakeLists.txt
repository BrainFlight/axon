cmake_minimum_required(VERSION 3.0.2)
project(grpc_navigation_node)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  geometry_msgs
  move_base_msgs
  actionlib
)

find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS 
    roscpp
    std_msgs
    geometry_msgs
    move_base_msgs
    actionlib
)

add_library(${PROJECT_NAME}
  src/grpc_ros_bridge.cpp
)

target_link_libraries(${PROJECT_NAME}
  ${catkin_LIBRARIES}
  gRPC::grpc++
  gRPC::grpc++_reflection
  protobuf::libprotobuf
)

add_executable(${PROJECT_NAME}_node src/main.cpp)

target_link_libraries(${PROJECT_NAME}_node
  ${PROJECT_NAME}
  ${catkin_LIBRARIES}
)

install(TARGETS ${PROJECT_NAME} ${PROJECT_NAME}_node
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Install headers
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.hpp"
)