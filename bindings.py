import sys
import pathlib

from ctypes import *


class C_Waypoint(Structure):
    _fields_ = [('x', c_double),
                ('y', c_double),
                ('heading', c_double)]

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

c_lib.make_waypoint.restype = C_Waypoint
wp = c_lib.make_waypoint()
print(wp)
