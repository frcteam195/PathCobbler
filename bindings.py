import pathlib
import time

from ctypes import *

from utils.waypoint import Waypoint


class C_Waypoint(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('heading', c_double),
                ('curvature', c_double)]

    def __init__(self, x=0.0, y=0.0, heading=0.0):
        self.x = x
        self.y = y
        self.heading = heading

    def __str__(self):
        return f'{self.x} {self.y} {self.heading}'


class C_WaypointArray(Structure):
    _fields_ = [('size', c_uint32),
                ('wp_ptr', POINTER(C_Waypoint))]

    def __init__(self, points: list[C_Waypoint]):
        self.size = len(points)
        self.wp_ptr = (C_Waypoint * self.size)(*points)

    def create_waypoints(self):
        if self.size > 0:
            self.waypoints = cast(self.wp_ptr, POINTER(C_Waypoint * self.size)).contents

    def free(self):
        c_lib.freeme(self.wp_ptr)


libname = pathlib.Path().absolute()
c_lib = CDLL(libname / 'lib/build/libck_pathcobbler_bindings.dylib')

c_lib.freeme.argtypes = [c_void_p]
c_lib.calc_splines.argtypes = [C_WaypointArray]
c_lib.calc_splines.restype = C_WaypointArray


def calc_splines(waypoints: list[Waypoint]):
    if len(waypoints) < 2:
        return waypoints

    c_waypoints = []
    for wp in waypoints:
        if wp.enabled:
            c_waypoints.append(C_Waypoint(wp.x, wp.y, -wp.heading))

    c_wp_arr = C_WaypointArray(c_waypoints)

    start = time.time()
    spline_points: C_WaypointArray = c_lib.calc_splines(c_wp_arr)
    end = time.time()
    spline_points.create_waypoints()

    # print(f'Time to calc splines: {end - start} seconds')

    if spline_points.size == 0:
        return waypoints

    ret_wps = []
    for point in spline_points.waypoints:
        ret_wps.append(Waypoint(point.x, point.y, point.heading))
        # print(point)

    spline_points.free()

    return ret_wps


# c_lib.get_waypoints.restype = C_WaypointArray
# wp_arr: C_WaypointArray = c_lib.get_waypoints()

# print(wp_arr.size)

# wp_arr.create_waypoints()

# for wp in wp_arr.waypoints:
#     print(wp)

# print('\n')


# py_points = [C_Waypoint(1, 2, 3), C_Waypoint(4, 5, 6)]
# py_arr = (C_Waypoint * len(py_points))(*py_points)

# param = C_WaypointArray()
# param.wp_ptr = py_arr
# param.size = len(py_points)

# param = C_WaypointArray(py_points)

# wp_arr2: C_WaypointArray = c_lib.calc_splines(param)
# wp_arr2.create_waypoints()

# print('\n\n')
# for wp in wp_arr2.waypoints:
    # print(wp)
# print('\n\n')

# wp_arr.free()
# wp_arr2.free()
