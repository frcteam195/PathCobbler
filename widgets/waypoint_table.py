from PySide6 import QtWidgets

from widgets.waypoint import Waypoint
from widgets.waypoint_table_body import WaypointTableBody


class WaypointTable(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # self.setMinimumSize(300, 500)
        self.setMinimumWidth(500)
        # self.setMinimumHeight(300)

        self.heading_layout = QtWidgets.QHBoxLayout()
        x_label = QtWidgets.QLabel('X')
        y_label = QtWidgets.QLabel('Y')
        heading_label = QtWidgets.QLabel('Heading')
        enabled_label = QtWidgets.QLabel('Enabled')
        delete_label = QtWidgets.QLabel('Delete')

        self.heading_layout.addWidget(x_label)
        self.heading_layout.addWidget(y_label)
        self.heading_layout.addWidget(heading_label)
        self.heading_layout.addWidget(enabled_label)
        self.heading_layout.addWidget(delete_label)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.tableBody = WaypointTableBody()
        self.scroll_area.setWidget(self.tableBody)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.heading_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

    def update(self):
        self.waypoints = []

        for i in range(1, self.grid_layout.rowCount()):
            x_val = self.grid_layout.itemAtPosition(i, 0).widget().text()
            y_val = self.grid_layout.itemAtPosition(i, 1).widget().text()
            heading_val = self.grid_layout.itemAtPosition(i, 2).widget().text()
            enabled_val = self.grid_layout.itemAtPosition(i, 3).widget().isChecked()

            self.waypoints.append(Waypoint(x_val, y_val, heading_val, enabled_val))

    def get_waypoints(self) -> list[Waypoint]:
        return self.tableBody.get_waypoints()

    def add_waypoint(self, wp: Waypoint):
        self.tableBody.add_waypoint(wp)
