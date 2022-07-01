#pragma once

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

void waypoint_test(waypoint_t wp);
waypoint_t make_waypoint();
waypoint_t *make_waypoints(int size);
waypoint_t *sorcery(int *size);
void freeme(void *ptr);
void mod_waypoints(waypoint_t *wps, int size);
void print_num(int x);

#ifdef __cplusplus
}
#endif
