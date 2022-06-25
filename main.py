import sys

from PySide6 import QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
