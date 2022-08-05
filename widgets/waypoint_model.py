from utils.waypoint import Waypoint

from PySide6.QtCore import *


class WaypointModel():
    updated = Signal()

    def __init__(self, wapyoints: list[Waypoint]=None):
        self.waypoints: list[Waypoint] = wapyoints or []

    def __len__(self):
        return len(self.waypoints)

    def __getitem__(self, index):
        return self.waypoints[index]

    def __setitem__(self, index, wp: Waypoint):
        self.waypoints[index] = wp
        self.updated.emit()

    def __delitem__(self, index):
        del self.waypoints[index]
        self.updated.emit()
