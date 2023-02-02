from typing import List


from utils.waypoint import Waypoint

from threading import Lock


from PySide6.QtCore import QObject, Signal, QMutex

import traceback

class WaypointModel(QObject):
    updated = Signal()

    def __init__(self, wapyoints: List[Waypoint]=[]):
       
        super().__init__()
        self.waypoints: List[Waypoint] = wapyoints
        self.mutex = QMutex()

    def update(self, waypoints: List[Waypoint]=[]):
        if len(waypoints) > 0:
            self.waypoints = waypoints
        traceback.print_stack()
        self.mutex.lock()
        self.updated.emit()
        self.mutex.unlock()
                 

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
