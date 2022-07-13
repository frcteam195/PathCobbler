import sys
import pathlib

from ctypes import *


libname = pathlib.Path().absolute()
c_lib = CDLL(libname / 'lib/build/libck_pathcobbler_bindings.dylib')

c_lib.freeme.argtypes = [c_void_p]

class C_Waypoint(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('heading', c_double)]

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
        self.waypoints = cast(self.wp_ptr, POINTER(C_Waypoint * self.size)).contents

    def free(self):
        c_lib.freeme(self.wp_ptr)


# c_lib.get_waypoints.restype = C_WaypointArray
# wp_arr: C_WaypointArray = c_lib.get_waypoints()

# print(wp_arr.size)

# wp_arr.create_waypoints()

# for wp in wp_arr.waypoints:
#     print(wp)

# print('\n')


py_points = [C_Waypoint(1, 2, 3), C_Waypoint(4, 5, 6)]
# py_arr = (C_Waypoint * len(py_points))(*py_points)

# param = C_WaypointArray()
# param.wp_ptr = py_arr
# param.size = len(py_points)

param = C_WaypointArray(py_points)

c_lib.calc_splines.argtypes = [C_WaypointArray]
c_lib.calc_splines.restype = C_WaypointArray
wp_arr2: C_WaypointArray = c_lib.calc_splines(param)
wp_arr2.create_waypoints()

# wp_arr.free()
wp_arr2.free()
