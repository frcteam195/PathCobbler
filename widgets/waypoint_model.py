from utils.waypoint import Waypoint

from PySide6.QtCore import *


class WaypointModel(QObject):
    updated = Signal()

    def __init__(self, wapyoints: list[Waypoint]=None):
        super().__init__()
        self.waypoints: list[Waypoint] = wapyoints or []

    def update(self, waypoints: list[Waypoint]=None):
        if waypoints is not None:
            self.waypoints = waypoints

        self.updated.emit()

    def append(self, wp: Waypoint):
        self.waypoints.append(wp)
        self.update()

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

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self):
            result = self[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration
