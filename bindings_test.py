from utils.bindings import calc_splines
from utils.waypoint import Waypoint

waypoints = [
    Waypoint(0, 0, 0),
    Waypoint(50, -50, 0)
]

wps = calc_splines(waypoints)

for wp in wps:
    print(wp)