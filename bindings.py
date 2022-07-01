import sys
import pathlib

from ctypes import *


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

libname = pathlib.Path().absolute()
c_lib = CDLL(libname / 'lib/build/libwaypoint_cpp.so')

x = 5

c_lib.print_num.argtypes = [c_int]
c_lib.print_num(x)

wp = C_Waypoint()
wp.x = 1.123
wp.y = 20
wp.heading = 30

c_lib.waypoint_test.argtypes = [C_Waypoint]
c_lib.waypoint_test(wp)

print('\n\n')

c_lib.make_waypoints.restype = c_void_p
wp = c_lib.make_waypoints(5)
# print(wp.contents[0])

wps = cast(wp, POINTER(C_Waypoint * 5))

# print(wps.contents[0])
for wp_a in wps.contents:
    print(wp_a)

# cast(wp, c_void_p)
c_lib.freeme.argtypes = [c_void_p]
c_lib.freeme(wp)

print('\n\n')

wps = []
for i in range(10):
    wps.append(C_Waypoint(0, i, 0))

wp_arr_t = C_Waypoint * len(wps)
wps_arr = wp_arr_t(*wps)

c_lib.mod_waypoints.argtypes = [wp_arr_t, c_int]
c_lib.mod_waypoints(wps_arr, len(wps))

for wp in wps_arr:
    print(wp)
