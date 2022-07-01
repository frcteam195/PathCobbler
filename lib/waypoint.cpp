#include "waypoint.hpp"
#include <iostream>

void waypoint_test(waypoint_t wp)
{
    std::cout << "X: " << wp.x
              << ", Y: " << wp.y
              << ", Heading: " << wp.heading
              << std::endl;
}

waypoint_t make_waypoint()
{
    waypoint_t wp = {10, 20, 45};
    return wp;
}

void print_num(int x)
{
    std::cout << "CPP: " << x << std::endl;
}
