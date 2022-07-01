#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

typedef struct
{
    double x;
    double y;
    double heading;
} waypoint_t;

typedef struct
{
    uint32_t size;
    waypoint_t *wp_ptr;
} waypoint_array_t;

void waypoint_test(waypoint_t wp);
waypoint_t make_waypoint();
waypoint_t *make_waypoints(int size);
waypoint_t *sorcery(int *size);
waypoint_array_t get_waypoints();
void freeme(void *ptr);
void mod_waypoints(waypoint_t *wps, int size);
void print_num(int x);

#ifdef __cplusplus
}
#endif
