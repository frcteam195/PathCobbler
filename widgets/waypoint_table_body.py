from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel


class WaypointTableBody(QWidget):
    updateSignal = Signal(list, name='updateSignal')

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.waypoints = []
        self.model = model
        self.model.updated.connect(self.draw_table)

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.grid_layout)

    def update(self):
        waypoints = []

        for i in range(1, self.grid_layout.rowCount()):
            x_val = float(self.grid_layout.itemAtPosition(i, 0).widget().text())
            y_val = float(self.grid_layout.itemAtPosition(i, 1).widget().text())
            heading_val = float(self.grid_layout.itemAtPosition(i, 2).widget().text())
            enabled_val = self.grid_layout.itemAtPosition(i, 3).widget().isChecked()

            waypoints.append(Waypoint(x_val, y_val, heading_val, enabled=enabled_val))

        self.model.update(waypoints)

    def draw_table(self):
        self.clear()
        # self.create_heading()

        for wp in self.model:
            self.add_waypoint(wp)

    def get_waypoints(self) -> list[Waypoint]:
        self.update()
        return self.waypoints

    def create_heading(self):
        x_label = QLabel('X')
        x_label.setAlignment(Qt.AlignCenter)

        y_label = QLabel('Y')
        y_label.setAlignment(Qt.AlignCenter)

        heading_label = QLabel('Heading')
        heading_label.setAlignment(Qt.AlignCenter)

        enabled_label = QLabel('Enabled')
        enabled_label.setAlignment(Qt.AlignCenter)

        delete_label = QLabel('Delete')
        delete_label.setAlignment(Qt.AlignCenter)

        self.grid_layout.addWidget(x_label, 0, 0)
        self.grid_layout.addWidget(y_label, 0, 1)
        self.grid_layout.addWidget(heading_label, 0, 2)
        self.grid_layout.addWidget(enabled_label, 0, 3)
        self.grid_layout.addWidget(delete_label, 0, 4)

    def add_waypoint(self, wp: Waypoint):
        numRows = self.grid_layout.rowCount()

        # TODO: Fix model implementation so the
        # textChanged signal can be used instead of
        # editing finished.

        x_label = QLabel('X:')
        x_input = QLineEdit(str(wp.x))
        x_input.setAlignment(Qt.AlignCenter)
        x_input.editingFinished.connect(self.update)

        y_label = QLabel('Y:')
        y_input = QLineEdit(str(wp.y))
        y_input.setAlignment(Qt.AlignCenter)
        y_input.editingFinished.connect(self.update)

        heading_label = QLabel('Heading:')
        heading_input = QLineEdit(str(wp.heading))
        heading_input.setAlignment(Qt.AlignCenter)
        heading_input.editingFinished.connect(self.update)

        enabled_label = QLabel('Enabled?:')
        enabled_input = QCheckBox()
        enabled_input.setChecked(wp.enabled)
        enabled_input.stateChanged.connect(self.update)

        delete_label = QLabel('Delete')
        delete_input = QPushButton('X')
        delete_input.clicked.connect(lambda: self.delete_row(numRows))

        self.grid_layout.addWidget(x_input, numRows, 0)
        self.grid_layout.addWidget(y_input, numRows, 1)
        self.grid_layout.addWidget(heading_input, numRows, 2)
        self.grid_layout.addWidget(enabled_input, numRows, 3)
        self.grid_layout.addWidget(delete_input, numRows, 4)

        # self.grid_layout.addWidget(x_label, numRows, 0)
        # self.grid_layout.addWidget(x_input, numRows, 1)
        # self.grid_layout.addWidget(y_label, numRows, 2)
        # self.grid_layout.addWidget(y_input, numRows, 3)
        # self.grid_layout.addWidget(heading_label, numRows, 4)
        # self.grid_layout.addWidget(heading_input, numRows, 5)
        # # self.grid_layout.addWidget(enabled_label, numRows, 6)
        # self.grid_layout.addWidget(enabled_input, numRows, 7)
        # # self.grid_layout.addWidget(delete_label, numRows, 8)
        # self.grid_layout.addWidget(delete_input, numRows, 9)

    def delete_row(self, rowNum):
        # waypoints = self.get_waypoints()
        # del waypoints[rowNum - 1]
        del self.model[rowNum - 1]

        self.draw_table()

        # tempWidget = QWidget()
        # tempWidget.setLayout(self.grid_layout)
        # tempWidget.deleteLater()

        # self.grid_layout = QGridLayout()
        # self.grid_layout.setAlignment(Qt.AlignTop)

        # for wp in waypoints:
        #     self.add_waypoint(wp)

        # self.setLayout(self.grid_layout)
        # self.update()

    def clear(self):
        tempWidget = QWidget()
        tempWidget.setLayout(self.grid_layout)
        tempWidget.deleteLater()

        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.grid_layout)
