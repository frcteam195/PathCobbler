import os
import sys
import time
import signal

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from widgets.main_widget import MainWidget


signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PathCobbler 🥧")
        self.control = MainWidget()
        self.setCentralWidget(self.control)

        logoPath = os.path.join(os.path.dirname(__file__), 'resources/img/logo.png')

        self.setWindowIcon(QPixmap(logoPath))

        splashScreen = QSplashScreen(QPixmap(logoPath))
        splashScreen.show()
        time.sleep(0.4)


if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
