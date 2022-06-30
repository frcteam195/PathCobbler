import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        self.image = QPixmap("resources/img/field.png").scaledToWidth(800)
        self.setGeometry(100, 100, 500, 300)
        self.resize(self.image.width(), self.image.height())
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            painter = QPainter(self.image)
            # painter.setPen(QPen(Qt.red, 10, Qt.SolidLine))
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
            size = 8
            painter.drawEllipse(event.position(), size, size)
            self.update()
            # self.drawing = True
            # self.lastPoint = event.position()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)

            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.position())
            self.lastPoint = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec())
