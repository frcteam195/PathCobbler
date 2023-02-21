from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from typing import List

class Auto(QListWidgetItem):
    def __init__(self, name, waypoints: List[Waypoint]):
        super().__init__(name)
        self.setFlags(self.flags() | Qt.ItemFlag.ItemIsEditable)
        self.waypoints: List[Waypoint] = waypoints

