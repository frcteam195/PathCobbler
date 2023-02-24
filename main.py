import os
import sys
import time
import signal

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from widgets.main_widget import MainWidget


signal.signal(signal.SIGINT, signal.SIG_DFL)


# import faulthandler
# faulthandler.enable()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PathCobbler 🥧")
        self.control = MainWidget()
        self.setCentralWidget(self.control)

        logoPath = os.path.join(os.path.dirname(__file__), 'resources/images/logo.png')

        self.setWindowIcon(QPixmap(logoPath))

        splashScreen = QSplashScreen(QPixmap(logoPath))
        splashScreen.show()
        time.sleep(0.4)

    def move_window_to_center(self):
        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())


if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    mw.move_window_to_center()
    sys.exit(app.exec())
