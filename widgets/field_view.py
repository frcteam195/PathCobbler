import os
import sys
import math

from typing import List

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

import utils.constants as constants
from utils.waypoint import Waypoint
from utils.translation2d import Translation2d
from utils.bindings import calc_splines
from widgets.waypoint_model import WaypointModel
import numpy as np


base_dir = os.path.dirname(os.path.dirname(__file__))


class FieldView(QLabel):
    pointAdded = Signal(Waypoint, name='pointAdded')

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.setMouseTracking(True)

        self.model = model
        self.model.updated.connect(lambda: self.draw_waypoints(self.model.waypoints))

        self.currentWaypoints = []
        self.is_flipped = False

        self.img_path = f'{base_dir}/resources/images/field.png'
        self.img_path_flipped = f'{base_dir}/resources/images/fieldFlipped.png'
        self.scaled_width = 1200

        self.image = QPixmap(self.img_path).scaledToWidth(self.scaled_width)
        self.setPixmap(self.image)

        self.fieldWidth = self.image.width()
        self.fieldHeight = self.image.height()

        self.wp_size = 8
        self.track_length = 15
        self.painter = QPainter()

        self.rotate_heading = False
        self.rotate_track = False
        self.hover_point = False
        self.setFocusPolicy(Qt.ClickFocus)

    def pixels_to_inches(self, pixelsX, pixelsY):
        inchesX = (pixelsX / self.fieldWidth) * constants.fieldWidth - constants.xOffset
        inchesY = constants.fieldHeight - (pixelsY / self.fieldHeight) * constants.fieldHeight - constants.yOffset

        return (inchesX, inchesY)

    def inches_to_pixels(self, inchesX, inchesY):
        pixelsX = (inchesX + constants.xOffset) / constants.fieldWidth * self.fieldWidth
        pixelsY = self.fieldHeight - (inchesY + constants.yOffset) / constants.fieldHeight * self.fieldHeight

        return (pixelsX, pixelsY)

    def flip_field(self):
        self.is_flipped = not self.is_flipped

        if self.is_flipped:
            self.image = QPixmap(self.img_path_flipped).scaledToWidth(self.scaled_width)
        else:
            self.image = QPixmap(self.img_path).scaledToWidth(self.scaled_width)

        self.setPixmap(self.image)

        self.draw_waypoints(self.currentWaypoints)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        if ev.button() == Qt.LeftButton:
            for wp in self.model:
                if not wp.enabled:
                    continue

                pixelsX, pixelsY = self.inches_to_pixels(wp.x, wp.y)

                dist = math.hypot(pixelsX - ev.position().x(), pixelsY - ev.position().y())

                if dist < self.wp_size:
                    wp.set_clicked(True)
                    self.model.update()
                    return

            track = 0
            heading = 0

            inchesX, inchesY = self.pixels_to_inches(ev.position().x(), ev.position().y())
            inchesX = int(inchesX)
            inchesY = int(inchesY)

            if len(self.currentWaypoints) > 0:
                last_wp = self.currentWaypoints[-1]
                x_diff = inchesX - last_wp.x
                y_diff = inchesY - last_wp.y

                track = int(math.degrees(math.atan2(y_diff, x_diff)))

                heading = track

            wp = Waypoint(inchesX, inchesY, track, heading)

            self.model.append(wp)
        elif ev.button() == Qt.RightButton:
            spline_wps = calc_splines(self.model.waypoints)

            for wp in spline_wps:
                pixelsX, pixelsY = self.inches_to_pixels(wp.x, wp.y)

                dist = math.hypot(pixelsX - ev.position().x(), pixelsY - ev.position().y())

                if dist < 30:
                    print('found')




    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        for wp in self.model:
            wp.set_clicked(False)

        self.model.update()

        return super().mouseReleaseEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        inchesX, inchesY = self.pixels_to_inches(ev.position().x(), ev.position().y())
        inchesX = float(math.floor(inchesX))
        inchesY = float(math.floor(inchesY))
        for wp in self.model:
            if wp.clicked:
                self.setFocus()
                if self.rotate_track:
                    x_diff = inchesX - wp.x
                    y_diff = inchesY - wp.y

                    wp.track = float(math.floor(math.degrees(math.atan2(y_diff, x_diff))))

                elif self.rotate_heading:
                    x_diff = inchesX - wp.x
                    y_diff = inchesY - wp.y

                    wp.heading = float(math.floor(math.degrees(math.atan2(y_diff, x_diff))))
                else:
                    wp.x = inchesX
                    wp.y = inchesY
                self.model.update()
        if self.hover_point:
            inchesX = float(math.floor(inchesX))
            inchesY = float(math.floor(inchesY))
            self.get_spline_distance(inchesX, inchesY)
            # self.setToolTip(self.get_spline_distance(inchesX, inchesY))
            pos = QPoint(ev.globalX(), ev.globalY())
            QToolTip.showText(pos, self.get_spline_distance(inchesX, inchesY))

        return super().mouseMoveEvent(ev)

    def clear_canvas(self):
        self.setPixmap(self.image)

    def draw_waypoints(self, wps: List[Waypoint]):
        spline_wps = calc_splines(wps)

        self.currentWaypoints = wps
        self.clear_canvas()

        canvas = self.pixmap()
        self.painter = QPainter(canvas)
        self.painter.setRenderHint(QPainter.Antialiasing)

        for wp in spline_wps:
            if wp.enabled:
                pixelsX, pixelsY = self.inches_to_pixels(wp.x, wp.y)

                self.painter.setPen(Qt.NoPen)
                self.painter.setBrush(QBrush(QColor(0, 255, 0), Qt.SolidPattern))
                self.painter.drawEllipse(QPointF(pixelsX, pixelsY), 3, 3)
                self.drawRobot(self.painter, wp)

        for idx, wp in enumerate(spline_wps):
            if wp.enabled:
                pixelsX, pixelsY = self.inches_to_pixels(wp.x, wp.y)

                if idx % 10 == 0:
                    heading_x_d = self.track_length * math.cos(math.radians(wp.heading))
                    heading_y_d = self.track_length * math.sin(math.radians(wp.heading))
                    self.painter.setPen(QPen(QColor(255, 0, 0), 3))
                    self.painter.drawLine(QPointF(pixelsX, pixelsY), QPointF(pixelsX + heading_x_d, pixelsY - heading_y_d))

        for wp in wps:
            if wp.enabled:
                pointColor = QColor(25, 255, 45)
                lineColor = pointColor
                headingColor = QColor(250, 17, 242)

                if wp.clicked:
                    pointColor = QColor(255, 0, 0)

                    if self.rotate_heading:
                        lineColor = pointColor
                    if self.rotate_track:
                        headingColor = QColor(255, 172, 28)

                pixelsX, pixelsY = self.inches_to_pixels(wp.x, wp.y)

                x_diff = self.track_length * math.cos(math.radians(wp.track))
                y_diff = self.track_length * math.sin(math.radians(wp.track))
                heading_x_d = self.track_length * math.cos(math.radians(wp.heading))
                heading_y_d = self.track_length * math.sin(math.radians(wp.heading))

                self.painter.setPen(QPen(lineColor, 3))
                self.painter.drawLine(QPointF(pixelsX, pixelsY), QPointF(pixelsX + x_diff, pixelsY - y_diff))
                self.painter.setPen(QPen(headingColor, 3))
                self.painter.drawLine(QPointF(pixelsX, pixelsY), QPointF(pixelsX + heading_x_d , pixelsY - heading_y_d))
                self.painter.setPen(Qt.NoPen)
                self.painter.setBrush(QBrush(pointColor, Qt.SolidPattern))
                self.painter.drawEllipse(QPointF(pixelsX, pixelsY), self.wp_size, self.wp_size)

        self.painter.end()
        self.setPixmap(canvas)

    def drawRobot(self, painter: QPainter, wp: Waypoint):
        h = math.radians(wp.heading)

        angles = [h + (math.pi / 2) + constants.C_T,
                h - (math.pi / 2) + constants.C_T,
                h + (math.pi / 2) - constants.C_T,
                h - (math.pi / 2) - constants.C_T]

        # TODO: Try to only use 1 translation2d instance to do this
        # need to convert C_R to pixels somehow?
        for angle in angles:
            point = Translation2d(wp.x + (constants.C_R * math.cos(angle)),
                                wp.y + (constants.C_R * math.sin(angle)))

            color = QColor(0, 170, 255) if abs(angle - h) < math.pi / 2 else QColor(0, 102, 255)

            pixelsX, pixelsY = self.inches_to_pixels(point.x, point.y)

            pixelPoint = Translation2d(pixelsX, pixelsY)

            pixelPoint.draw(painter, color, 2)
    def get_spline_distance(self, x, y):
        distances = []
        wps_list = calc_splines(self.model.waypoints)
        if len(wps_list) > 1:
            for idx, wps in enumerate(wps_list):
                if idx < len(wps_list):
                    point1 = np.array([wps_list[idx].x, wps_list[idx].y], dtype=float)
                    point2 = np.array([x, y], dtype=float)
                    current_distance = np.linalg.norm(point1-point2)
                    distances.append(current_distance)
            # print(np.argmin(distances))
            # print(len(wps_list)-1)
            return f"{np.round(((np.argmin(distances))/(len(wps_list)-1))*100, 1)}%"
