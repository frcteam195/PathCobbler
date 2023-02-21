from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from typing import List

class Auto(QListWidgetItem):
    def __init__(self, name, waypoints: List[Waypoint]):
        super().__init__(name)
        self.name = name
        self.waypoints: List[Waypoint] = waypoints
    
    def set_name(self, new_name):
        self.setText(new_name)