from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Auto(QListWidgetItem):
    def __init__(self, name, waypoints):
        super().__init__(name)
        self.name = name
        self.waypoints = waypoints