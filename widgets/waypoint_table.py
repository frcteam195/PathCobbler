import numbers
from PySide6 import QtWidgets

from widgets.waypoint import Waypoint


class WaypointTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.waypoints = []

        self.header_layout = QtWidgets.QHBoxLayout()
        self.create_table_heading2()

        self.grid_layout = QtWidgets.QGridLayout()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.grid_layout)

        self.setLayout(self.main_layout)

    def create_table_heading2(self):
        print('creating heading')
        x_label = QtWidgets.QLabel('X')
        y_label = QtWidgets.QLabel('Y')
        heading_label = QtWidgets.QLabel('Heading')
        enabled_label = QtWidgets.QLabel('Enabled')
        delete_label = QtWidgets.QLabel('Delete')

        self.header_layout.addWidget(x_label)
        self.header_layout.addWidget(y_label)
        self.header_layout.addWidget(heading_label)
        self.header_layout.addWidget(enabled_label)
        self.header_layout.addWidget(delete_label)

    def create_table_heading(self):
        print('creating heading')
        x_label = QtWidgets.QLabel('X')
        y_label = QtWidgets.QLabel('Y')
        heading_label = QtWidgets.QLabel('Heading')
        enabled_label = QtWidgets.QLabel('Enabled')
        delete_label = QtWidgets.QLabel('Delete')

        self.grid_layout.addWidget(x_label, 0, 0)
        self.grid_layout.addWidget(y_label, 0, 1)
        self.grid_layout.addWidget(heading_label, 0, 2)
        self.grid_layout.addWidget(enabled_label, 0, 3)
        self.grid_layout.addWidget(delete_label, 0, 4)

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
        # waypoints = self.get_waypoints()
        # del waypoints[rowNum - 1]

        # tempWidget = QtWidgets.QWidget()
        # tempWidget.setLayout(self.grid_layout)
        # tempWidget.deleteLater()

        # self.grid_layout = QtWidgets.QGridLayout()

        # for wp in waypoints:
        #     self.add_waypoint(wp)

        # print(self.main_layout.itemAt(1).layout().rowCount())

        grid = self.main_layout.itemAt(0)
        # self.main_layout.removeItem(grid)
        grid.deleteLater()

        # print(self.main_layout.itemAt(1))
        self.update()
