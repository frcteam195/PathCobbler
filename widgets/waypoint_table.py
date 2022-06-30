from PySide6.QtWidgets import *
from PySide6.QtCore import *

from widgets.waypoint import Waypoint
from widgets.waypoint_table_body import WaypointTableBody


class WaypointTable(QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 300)

        self.addButton = QPushButton('Add Point')
        self.addButton.clicked.connect(lambda: self.add_waypoint())
        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.update)
        self.animateButton = QPushButton('Animate')
        self.flipButton = QPushButton('Flip Field')

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.updateButton)
        self.buttonLayout.addWidget(self.animateButton)
        self.buttonLayout.addWidget(self.flipButton)

        self.heading_layout = QHBoxLayout()
        x_label = QLabel('X')
        y_label = QLabel('Y')
        heading_label = QLabel('Heading')
        enabled_label = QLabel('Enabled')
        delete_label = QLabel('Delete')

        self.heading_layout.addWidget(x_label)
        self.heading_layout.addWidget(y_label)
        self.heading_layout.addWidget(heading_label)
        self.heading_layout.addWidget(enabled_label)
        self.heading_layout.addWidget(delete_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.tableBody = WaypointTableBody()
        self.scroll_area.setWidget(self.tableBody)
        self.updateSignal = self.tableBody.updateSignal

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.buttonLayout)
        self.main_layout.addLayout(self.heading_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

    def update(self):
        self.tableBody.update()

    def get_waypoints(self) -> list[Waypoint]:
        return self.tableBody.get_waypoints()

    def add_waypoint(self, wp: Waypoint=Waypoint(0, 0, 0)):
        self.tableBody.add_waypoint(wp)

    def delete_row(self, rowNum):
        self.tableBody.delete_row(rowNum)
