import sys

from PySide6 import QtWidgets

from widgets.waypoint import Waypoint
from widgets.waypoint_control import WaypointControl
from widgets.waypoint_table import WaypointTable

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.control = WaypointControl()

        # self.control.waypoint_table.tableBody.add_waypoint(Waypoint(0, 0, 45))
        # self.control.waypoint_table.add_waypoint(Waypoint(20, 20, 65))

        self.setCentralWidget(self.control)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
