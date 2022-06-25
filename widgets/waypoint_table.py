from sqlite3 import enable_shared_cache
from turtle import heading
from unittest import defaultTestLoader
from PySide6 import QtWidgets

from .waypoint import Waypoint

class WaypointTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        x_label = QtWidgets.QLabel('X')
        y_label = QtWidgets.QLabel('Y')
        heading_label = QtWidgets.QLabel('Heading')
        enabled_label = QtWidgets.QLabel('Enabled')
        delete_label = QtWidgets.QLabel('Delete')

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(x_label, 0, 0)
        self.grid_layout.addWidget(y_label, 0, 1)
        self.grid_layout.addWidget(heading_label, 0, 2)
        self.grid_layout.addWidget(enabled_label, 0, 3)
        self.grid_layout.addWidget(delete_label, 0, 4)

        self.setLayout(self.grid_layout)

    def add_waypoint(self, wp: Waypoint):
        x_input = QtWidgets.QLineEdit(str(wp.x))
        y_input = QtWidgets.QLineEdit(str(wp.y))
        heading_input = QtWidgets.QLineEdit(str(wp.heading))
        enabled_input = QtWidgets.QCheckBox()
        enabled_input.setChecked(wp.enabled)
        delete_input = QtWidgets.QPushButton('X')

        numRows = self.grid_layout.rowCount()

        self.grid_layout.addWidget(x_input, numRows, 0)
        self.grid_layout.addWidget(y_input, numRows, 1)
        self.grid_layout.addWidget(heading_input, numRows, 2)
        self.grid_layout.addWidget(enabled_input, numRows, 3)
        self.grid_layout.addWidget(delete_input, numRows, 4)
