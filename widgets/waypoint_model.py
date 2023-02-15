from typing import List


from utils.waypoint import Waypoint

from PySide6.QtCore import QObject, Signal

class WaypointModel(QObject):
    updated = Signal()

    def __init__(self, waypoints: List[Waypoint]=[]):
       
        super().__init__()
        self.waypoints: List[Waypoint] = waypoints

    def update(self, waypoints: List[Waypoint]=[]):
        if waypoints is not None:
            if len(waypoints) > 0:
                self.waypoints = waypoints
            self.updated.emit()

    def clear_model(self):
        self.waypoints.clear()
        self.updated.emit()
                 

    def append(self, wp: Waypoint):
        wps = self.waypoints+[wp]
        
        self.update(wps)

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
