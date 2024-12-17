#pragma once
#include <string>
#include <vector>

struct NavigationAction {
    std::string name;
    std::vector<std::string> keywords;
    int floor;
};

struct Action {
    NavigationAction navigation;
};
