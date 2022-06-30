from dataclasses import field
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from widgets.field_view import FieldView
from widgets.waypoint import Waypoint
from widgets.waypoint_table import WaypointTable


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.field = FieldView()
        self.field.pointAdded.connect(self.add_click_wp_to_table)
        button = QPushButton('Push me')
        button.clicked.connect(lambda: self.field.clear_canvas())

        self.table = WaypointTable()
        self.table.updateSignal.connect(self.update_field_waypoints)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.field, alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.table, alignment=Qt.AlignHCenter)
        # self.mainLayout.addWidget(button)

        self.setLayout(self.mainLayout)

    def add_click_wp_to_table(self, wp: Waypoint):
        self.table.add_waypoint(wp)

    def update_field_waypoints(self, wps: list[Waypoint]):
        self.field.draw_waypoints(wps)
