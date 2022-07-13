import os
import math

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint

from bindings import calc_splines


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

        self.wp_size = 8
        self.heading_length = 15
        self.painter = QPainter()

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

        # TODO: set heading to the angle that points from the last point to the new point
        heading = self.currentWaypoints[-1].heading if len(self.currentWaypoints) > 0 else 0
        wp = Waypoint(ev.position().x(), ev.position().y(), heading)
        self.pointAdded.emit(wp)

    def clear_canvas(self):
        self.setPixmap(self.image)

    def draw_waypoints(self, wps: list[Waypoint]):
        spline_wps = calc_splines(wps)

        self.currentWaypoints = wps
        self.clear_canvas()

        canvas = self.pixmap()
        self.painter = QPainter(canvas)
        self.painter.setRenderHint(QPainter.Antialiasing)

        for wp in spline_wps:
            self.painter.setPen(Qt.NoPen)
            self.painter.setBrush(QBrush(QColor(0, 0, 255), Qt.SolidPattern))
            self.painter.drawEllipse(QPointF(wp.x, wp.y), 4, 4)

        self.painter.setBrush(QBrush(QColor(25, 255, 45), Qt.SolidPattern))

        for wp in wps:
            if wp.enabled:
                self.painter.setPen(Qt.NoPen)
                self.painter.drawEllipse(QPointF(wp.x, wp.y), self.wp_size, self.wp_size)

                x_diff = self.heading_length * math.cos(math.radians(wp.heading))
                y_diff = self.heading_length * math.sin(math.radians(wp.heading))

                # painter.drawArc(wp.x, wp.y, 20, 0, 0, 1000)

                self.painter.setPen(QPen(Qt.green, 3))
                self.painter.drawLine(QPointF(wp.x, wp.y), QPointF(wp.x + x_diff, wp.y - y_diff))

        self.painter.end()
        self.setPixmap(canvas)
