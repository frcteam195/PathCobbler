import sys

from PySide6 import QtWidgets

from widgets.waypoint import Waypoint
from widgets.waypoint_control import WaypointControl
from widgets.waypoint_table import WaypointTable

import signal


signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.control = WaypointControl()

        self.setCentralWidget(self.control)

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
