#pragma once

typedef struct
{
    double x;
    double y;
    double heading;
} waypoint_t;

void waypoint_test(waypoint_t wp);
void print_num(int x);

// extern "C"
// {
//     void waypoint_test(way)
// }