from dataclasses import field
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from widgets.field_view import FieldView
from widgets.waypoint import Waypoint
from widgets.waypoint_control import WaypointControl


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.field = FieldView()
        self.field.pointAdded.connect(self.handle_add_waypoint)

        self.control = WaypointControl()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.field, alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.control, alignment=Qt.AlignHCenter)

        self.setLayout(self.mainLayout)

    def handle_add_waypoint(self, wp: Waypoint):
        self.control.waypoint_table.tableBody.add_waypoint(wp)
