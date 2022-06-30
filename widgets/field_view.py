from email.mime import base
import os

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from widgets.waypoint import Waypoint


base_dir = os.path.dirname(os.path.realpath(__file__))


class FieldView(QLabel):
    pointAdded = Signal(Waypoint)

    def __init__(self):
        super().__init__()

        self.image = QPixmap('/Users/chris/git/ck/PathCobbler/resources/img/field.png').scaledToWidth(900)
        # self.image = QPixmap(600, 600)
        self.setPixmap(self.image)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        # if ev.button() == Qt.LeftButton:
        canvas = self.pixmap()
        painter = QPainter(canvas)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(25, 255, 45), Qt.SolidPattern))
        size = 8
        painter.drawEllipse(ev.position(), size, size)
        painter.end()
        self.setPixmap(canvas)

        wp = Waypoint(ev.position().x(), ev.position().y(), 45)
        self.pointAdded.emit(wp)