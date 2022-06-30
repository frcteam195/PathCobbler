from PySide6 import QtWidgets

from utils.waypoint import Waypoint
from widgets.waypoint_table import WaypointTable


class WaypointControl(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.waypoint_table = WaypointTable()

        self.addButton = QtWidgets.QPushButton('Add Point')
        self.addButton.clicked.connect(self.add_button_handler)
        self.updateButton = QtWidgets.QPushButton('Update')
        self.updateButton.clicked.connect(self.waypoint_table.update)
        self.animateButton = QtWidgets.QPushButton('Animate')
        self.flipButton = QtWidgets.QPushButton('Flip Field')

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.updateButton)
        self.buttonLayout.addWidget(self.animateButton)
        self.buttonLayout.addWidget(self.flipButton)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addWidget(self.waypoint_table)

        self.setLayout(self.mainLayout)

    def add_button_handler(self):
        self.waypoint_table.add_waypoint(Waypoint(0, 0, 0))
