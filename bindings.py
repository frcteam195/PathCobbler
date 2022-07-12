import sys
import pathlib

from ctypes import *


libname = pathlib.Path().absolute()
c_lib = CDLL(libname / 'lib/build/libck_pathcobbler_bindings.so')

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

    def create_waypoints(self):
        self.waypoints = cast(self.wp_ptr, POINTER(C_Waypoint * self.size)).contents

    def free(self):
        c_lib.freeme(self.wp_ptr)


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

# c_lib.make_waypoints.restype = c_void_p
c_lib.make_waypoints.restype = POINTER(C_Waypoint)
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


print('\n\n')

x = c_int(0)

c_lib.sorcery.argtypes = [POINTER(c_int)]
c_lib.sorcery.restype = POINTER(C_Waypoint)
wp_ptr = c_lib.sorcery(pointer(x))

print(x.value)

wps = cast(wp_ptr, POINTER(C_Waypoint * x.value))

for wp in wps.contents:
    print(wp)

c_lib.freeme(wp_ptr)

print('\n\n')

c_lib.get_waypoints.restype = C_WaypointArray
wp_arr: C_WaypointArray = c_lib.get_waypoints()

print(wp_arr.size)

wp_arr.create_waypoints()

for wp in wp_arr.waypoints:
    print(wp)

wp_arr.free()
