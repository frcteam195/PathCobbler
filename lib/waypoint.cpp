#include "waypoint.h"
#include <iostream>

void waypoint_test(waypoint_t wp)
{
    std::cout << "X: " << wp.x
              << ", Y: " << wp.y
              << ", Heading: " << wp.heading
              << std::endl;
}

void print_num(int x)
{
    std::cout << "CPP: " << x << std::endl;
}
