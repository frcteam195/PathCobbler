#include "waypoint.hpp"
#include <iostream>
#include <stdio.h>

#include "trajectory_generator_node/include/Constants.hpp"

void waypoint_test(waypoint_t wp)
{
    std::cout << K_DRIVE_WHEEL_DIAMETER_INCHES << std::endl;

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

waypoint_t *make_waypoints(int size)
{
    waypoint_t *wps = new waypoint_t[size];

    printf("Allocating address: %p\n", wps);

    for (int i = 0; i < size; i++)
    {
        wps[i].x = i * 1.0;
        wps[i].y = i * 2.0;
        wps[i].heading = i * 3.0;
    }

    return wps;
}

waypoint_t *sorcery(int *size)
{
    *size = 10;
    return make_waypoints(*size);
}

waypoint_array_t get_waypoints()
{
    waypoint_array_t wp_arr;
    wp_arr.size = 15;
    wp_arr.wp_ptr = make_waypoints(wp_arr.size);
    return wp_arr;
}

void freeme(void *ptr)
{
    printf("Freeing address: %p\n", ptr);
    free(ptr);
}

void mod_waypoints(waypoint_t *wps, int size)
{
    for (int i = 0; i < size; i++)
    {
        wps[i].x = 100;
        wps[i].heading = 2.0 * i;
    }
}

void print_num(int x)
{
    std::cout << "CPP: " << x << std::endl;
}
