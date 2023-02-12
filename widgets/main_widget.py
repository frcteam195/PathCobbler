from typing import List

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from widgets.field_view import FieldView
from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel
from widgets.waypoint_table import WaypointTable


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.model = WaypointModel()

        self.field = FieldView(self.model)
        self.field.pointAdded.connect(self.add_click_wp_to_table)
        button = QPushButton('Push me')
        button.clicked.connect(lambda: self.field.clear_canvas())

        self.table = WaypointTable(self.model, self.field)
        self.table.updateSignal.connect(self.update_field_waypoints)
        self.table.flipSignal.connect(self.field.flip_field)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.field, alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.table, alignment=Qt.AlignHCenter)
        # self.mainLayout.addWidget(button)

        self.setLayout(self.mainLayout)

    def add_click_wp_to_table(self, wp: Waypoint):
        self.table.add_waypoint(wp)

    def update_field_waypoints(self, wps: List[Waypoint]):
        self.field.draw_waypoints(wps)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Shift:
            self.field.rotate_track = True
        if event.key() == Qt.Key_Control:
            self.field.rotate_heading = True
        return super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Shift:
            self.field.rotate_track = False
        if event.key() == Qt.Key_Control:
            self.field.rotate_heading = False
        return super().keyReleaseEvent(event)
