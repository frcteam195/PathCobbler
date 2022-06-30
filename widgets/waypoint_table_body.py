from PySide6.QtWidgets import *
from PySide6.QtCore import *

from widgets.waypoint import Waypoint


class WaypointTableBody(QWidget):
    updateSignal = Signal(list)

    def __init__(self):
        super().__init__()

        self.waypoints = []

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.grid_layout)

    def update(self):
        self.waypoints = []

        for i in range(1, self.grid_layout.rowCount()):
            x_val = float(self.grid_layout.itemAtPosition(i, 0).widget().text())
            y_val = float(self.grid_layout.itemAtPosition(i, 1).widget().text())
            heading_val = float(self.grid_layout.itemAtPosition(i, 2).widget().text())
            enabled_val = self.grid_layout.itemAtPosition(i, 3).widget().isChecked()

            self.waypoints.append(Waypoint(x_val, y_val, heading_val, enabled_val))

        self.updateSignal.emit(self.waypoints)

    def get_waypoints(self) -> list[Waypoint]:
        self.update()
        return self.waypoints

    def add_waypoint(self, wp: Waypoint):
        numRows = self.grid_layout.rowCount()

        x_input = QLineEdit(str(wp.x))
        x_input.textChanged.connect(self.update)
        y_input = QLineEdit(str(wp.y))
        y_input.textChanged.connect(self.update)
        heading_input = QLineEdit(str(wp.heading))
        heading_input.textChanged.connect(self.update)
        enabled_input = QCheckBox()
        enabled_input.setChecked(wp.enabled)
        enabled_input.stateChanged.connect(self.update)
        delete_input = QPushButton('X')
        delete_input.clicked.connect(lambda: self.delete_row(numRows))

        self.grid_layout.addWidget(x_input, numRows, 0)
        self.grid_layout.addWidget(y_input, numRows, 1)
        self.grid_layout.addWidget(heading_input, numRows, 2)
        self.grid_layout.addWidget(enabled_input, numRows, 3)
        self.grid_layout.addWidget(delete_input, numRows, 4)

        self.update()

    def delete_row(self, rowNum):
        waypoints = self.get_waypoints()
        del waypoints[rowNum - 1]

        tempWidget = QWidget()
        tempWidget.setLayout(self.grid_layout)
        tempWidget.deleteLater()

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)
        # self.create_table_heading()

        for wp in waypoints:
            self.add_waypoint(wp)

        self.setLayout(self.grid_layout)
        self.update()
