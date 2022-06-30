import sys
import signal

from PySide6.QtWidgets import *
from widgets.main_widget import MainWidget


signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PathCobbler 🥧")
        self.control = MainWidget()
        self.setCentralWidget(self.control)

if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
