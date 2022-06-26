from PySide6 import QtWidgets, QtCore

from widgets.waypoint import Waypoint


class WaypointTableBody(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.waypoints = []

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)

        # self.add_waypoint(Waypoint(0, 0, 0))
        # self.add_waypoint(Waypoint(0, 0, 0))
        # self.add_waypoint(Waypoint(0, 0, 0))
        # self.add_waypoint(Waypoint(0, 0, 0))
        # self.add_waypoint(Waypoint(0, 0, 0))
        # self.add_waypoint(Waypoint(0, 0, 0))

        self.setLayout(self.grid_layout)

    def update(self):
        self.waypoints = []

        for i in range(1, self.grid_layout.rowCount()):
            x_val = self.grid_layout.itemAtPosition(i, 0).widget().text()
            y_val = self.grid_layout.itemAtPosition(i, 1).widget().text()
            heading_val = self.grid_layout.itemAtPosition(i, 2).widget().text()
            enabled_val = self.grid_layout.itemAtPosition(i, 3).widget().isChecked()

            self.waypoints.append(Waypoint(x_val, y_val, heading_val, enabled_val))

    def get_waypoints(self) -> list[Waypoint]:
        self.update()
        return self.waypoints

    def add_waypoint(self, wp: Waypoint):
        numRows = self.grid_layout.rowCount()

        x_input = QtWidgets.QLineEdit(str(wp.x))
        y_input = QtWidgets.QLineEdit(str(wp.y))
        heading_input = QtWidgets.QLineEdit(str(wp.heading))
        enabled_input = QtWidgets.QCheckBox()
        enabled_input.setChecked(wp.enabled)
        delete_input = QtWidgets.QPushButton('X')
        delete_input.clicked.connect(lambda: self.delete_row(numRows))

        self.grid_layout.addWidget(x_input, numRows, 0)
        self.grid_layout.addWidget(y_input, numRows, 1)
        self.grid_layout.addWidget(heading_input, numRows, 2)
        self.grid_layout.addWidget(enabled_input, numRows, 3)
        self.grid_layout.addWidget(delete_input, numRows, 4)

    def delete_row(self, rowNum):
        waypoints = self.get_waypoints()
        del waypoints[rowNum - 1]

        tempWidget = QtWidgets.QWidget()
        tempWidget.setLayout(self.grid_layout)
        tempWidget.deleteLater()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setAlignment(QtCore.Qt.AlignTop)
        # self.create_table_heading()

        for wp in waypoints:
            self.add_waypoint(wp)

        self.setLayout(self.grid_layout)
        self.update()
