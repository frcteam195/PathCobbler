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

        self.currentWaypoints = []
        self.is_flipped = False

        self.img_path = '/Users/chris/git/ck/PathCobbler/resources/img/field.png'
        self.img_path_flipped = '/Users/chris/git/ck/PathCobbler/resources/img/fieldFlipped.png'
        self.scaled_width = 1200

        self.image = QPixmap((self.img_path)).scaledToWidth(self.scaled_width)
        self.setPixmap(self.image)

    def flip_field(self):
        self.is_flipped = not self.is_flipped

        if self.is_flipped:
            self.image = QPixmap(self.img_path_flipped).scaledToWidth(self.scaled_width)
        else:
            self.image = QPixmap(self.img_path).scaledToWidth(self.scaled_width)

        self.setPixmap(self.image)

        self.draw_waypoints(self.currentWaypoints)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() != Qt.LeftButton:
            return

        canvas = self.pixmap()
        painter = QPainter(canvas)
        painter.setPen(Qt.NoPen)
        # painter.setBrush(QBrush(QColor(25, 255, 45), Qt.SolidPattern))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        size = 8
        painter.drawEllipse(ev.position(), size, size)
        painter.end()
        self.setPixmap(canvas)

        wp = Waypoint(ev.position().x(), ev.position().y(), 45)
        self.pointAdded.emit(wp)

    def clear_canvas(self):
        self.setPixmap(self.image)

    def draw_waypoints(self, wps: list[Waypoint]):
        self.currentWaypoints = wps
        self.clear_canvas()

        canvas = self.pixmap()
        painter = QPainter(canvas)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(25, 255, 45), Qt.SolidPattern))
        size = 8

        for wp in wps:
            if wp.enabled:
                painter.drawEllipse(QPointF(wp.x, wp.y), size, size)

        painter.end()
        self.setPixmap(canvas)
