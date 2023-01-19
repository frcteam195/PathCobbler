from typing import List

from utils.waypoint import Waypoint


class Path:
    def __init__(self, name: str, waypoints: List[Waypoint]=None):
        self.name = name
        self.waypoints: List[Waypoint] = waypoints or []
