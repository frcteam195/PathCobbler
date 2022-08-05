from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class WaypointList(QAbstractItemView):
    def __init__(self):
        super().__init__()

        self.model = WaypointModel()

        self.setModel(self.model)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(600, 400)

        self.waypointList = WaypointList()

        self.setCentralWidget(self.waypointList)








if __name__ == '__main__':
    app = QApplication()

    mw = MainWindow()
    mw.show()

    app.exec()
