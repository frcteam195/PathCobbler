#include "waypoint.hpp"
#include "ck_utilities/geometry/Pose2d.hpp"
#include "ck_utilities/geometry/Pose2dWithCurvature.hpp"
#include "ck_utilities/geometry/Rotation2d.hpp"
#include "ck_utilities/geometry/Translation2d.hpp"
#include "ck_utilities/spline/QuinticHermiteSpline.hpp"
#include "ck_utilities/spline/Spline.hpp"
#include "ck_utilities/spline/SplineGenerator.hpp"
#include <vector>
#include <iostream>
#include <stdio.h>

using namespace ck::geometry;
using namespace ck::spline;

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

waypoint_array_t calc_splines(waypoint_array_t waypoints)
{
    std::vector<Pose2d> points;

    for (int i = 0; i < waypoints.size; i++)
    {
        double x = waypoints.wp_ptr[i].x;
        double y = waypoints.wp_ptr[i].y;
        double heading = waypoints.wp_ptr[i].heading;

        std::cout << "X: " << x
                  << ", Y: " << y
                  << ", Heading: " << heading
                  << std::endl;

        Translation2d t2d(x, y);
        Pose2d p2d(t2d, Rotation2d::fromDegrees(heading));

        points.push_back(p2d);
    }

    std::cout << "Num points: " << points.size() << std::endl;

    waypoint_array_t wp_arr;
    wp_arr.size = points.size();
    wp_arr.wp_ptr = make_waypoints(wp_arr.size);
    return wp_arr;
}
