import os
import math

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from utils.translation2d import Translation2d
from bindings import calc_splines
from utils.constants import *
from widgets.waypoint_model import WaypointModel


base_dir = os.path.dirname(os.path.realpath(__file__))


class FieldView(QLabel):
    pointAdded = Signal(Waypoint, name='pointAdded')

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.model = model
        self.model.updated.connect(lambda: self.draw_waypoints(self.model.waypoints))

        self.currentWaypoints = []
        self.is_flipped = False

        file_path = os.path.dirname(__file__)

        self.img_path = f'{file_path}/../resources/img/field.png'
        self.img_path_flipped = f'{file_path}/../resources/img/fieldFlipped.png'
        self.scaled_width = 1200

        self.image = QPixmap(self.img_path).scaledToWidth(self.scaled_width)
        self.setPixmap(self.image)

        self.wp_size = 8
        self.heading_length = 15
        self.painter = QPainter()

        self.rotate = False

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

        for wp in self.model:
            if not wp.enabled:
                continue

            dist = math.hypot(wp.x - ev.position().x(), wp.y - ev.position().y())

            if dist < self.wp_size:
                wp.set_clicked(True)
                self.model.update()
                return

        heading = 0

        if len(self.currentWaypoints) > 0:
            last_wp = self.currentWaypoints[-1]
            x_diff = ev.position().x() - last_wp.x
            y_diff = ev.position().y() - last_wp.y

            heading = -int(math.degrees(math.atan2(y_diff, x_diff)))

        wp = Waypoint(ev.position().x(), ev.position().y(), heading)
        self.model.append(wp)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        for wp in self.model:
            wp.set_clicked(False)

        self.model.update()

        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        for wp in self.model:
            if wp.clicked:
                if self.rotate:
                    x_diff = ev.position().x() - wp.x
                    y_diff = ev.position().y() - wp.y

                    wp.heading = -int(math.degrees(math.atan2(y_diff, x_diff)))
                else:
                    wp.x = ev.position().x()
                    wp.y = ev.position().y()

        self.model.update()

        return super().mouseMoveEvent(ev)

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
            self.painter.setBrush(QBrush(QColor(0, 255, 0), Qt.SolidPattern))
            self.painter.drawEllipse(QPointF(wp.x, wp.y), 3, 3)

            self.drawRobot(self.painter, wp)

        for wp in wps:
            if wp.enabled:
                pointColor = QColor(25, 255, 45)
                lineColor = pointColor

                if wp.clicked:
                    pointColor = QColor(255, 0, 0)

                    if self.rotate:
                        lineColor = pointColor

                x_diff = self.heading_length * math.cos(math.radians(wp.heading))
                y_diff = self.heading_length * math.sin(math.radians(wp.heading))

                self.painter.setPen(QPen(lineColor, 3))
                self.painter.drawLine(QPointF(wp.x, wp.y), QPointF(wp.x + x_diff, wp.y - y_diff))

                self.painter.setPen(Qt.NoPen)
                self.painter.setBrush(QBrush(pointColor, Qt.SolidPattern))
                self.painter.drawEllipse(QPointF(wp.x, wp.y), self.wp_size, self.wp_size)

        self.painter.end()
        self.setPixmap(canvas)

    def drawRobot(self, painter: QPainter, wp: Waypoint):
        h = math.radians(wp.heading)
        angles = [h + (math.pi / 2) + C_T,
                  h - (math.pi / 2) + C_T,
                  h + (math.pi / 2) - C_T,
                  h - (math.pi / 2) - C_T]

        for angle in angles:
            point = Translation2d(wp.x + (C_R * math.cos(angle)),
                                  wp.y + (C_R * math.sin(angle)))

            color = QColor(0, 170, 255) if abs(angle - h) < math.pi / 2 else QColor(0, 102, 255)

            point.draw(painter, color, 2)
