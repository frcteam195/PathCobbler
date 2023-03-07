import os
import io
import json
import math
import time

from typing import List

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from io import BytesIO

import imageio as iio

from PIL import Image, ImageFont, ImageDraw

from utils.waypoint import Waypoint
from widgets.path_list import PathList
from widgets.waypoint_model import WaypointModel
from widgets.field_view import FieldView
from widgets.cordwainer import Cordwainer
# from widgets.TableWidgetDragRows import TableWidgetDragRows
from utils.auto import Auto

from utils.bindings import calc_splines

from utils.file_utils import *

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel
from copy import deepcopy, copy


class WaypointTableBody(QTableWidget):
    updateSignal = Signal(list, name='updateSignal')

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.waypoints = []
        self.model = model
        self.num_waypoints = 0
        # self.resize(500, 100)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setSelectionMode(QTableWidget.SingleSelection) 
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setDragDropMode(QTableWidget.InternalMove)   
        self.setDefaultDropAction(Qt.MoveAction)
        self.model.updated.connect(self.draw_table)
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["X", "Y", "Track", "Heading",  "Enabled", "Delete"])

        self.itemChanged.connect(self.item_changed)
    def dropEvent(self, event: QDropEvent):
        # print("drop event")
        self.blockSignals(True)
        delete_button_index = 5
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1
            delete_button = QPushButton("X")
            delete_button.clicked.connect(self.delete_row)
            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    if column_index == delete_button_index:
                        self.setCellWidget(row_index, delete_button_index, delete_button)
                        continue
                    self.setItem(row_index, column_index, column_data)
                    # print(row_index, column_index, column_data)
                
            event.accept()
            # for row_index in range(len(rows_to_move)):
            #     self.item(drop_row + row_index, 0).setSelected(True)
            #     self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)
        self.update()
        self.blockSignals(False)

        # self.update()

        # for i in range(self.rowCount()):
        #     self.dragUpdate(i)
        # self.update()

        # for r in range(0, self.rowCount()):
        #     print(f"Current Row: {r}")
        #     for c in range(0, self.columnCount()-1):
        #         print(f"Current Column: {c}")
        #         print(f"Item: {self.item(r, c).text()}")
        #         # print(f"")
    def getSelectedRows(self):
        selRows = []
        for item in self.selectedItems():
            if item.row() not in selRows:
                selRows.append(item.row())
        return selRows

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()

    def update(self):
        # print('updating')
        for i in range(0, self.rowCount()):
            # print(i)
            x_val = deepcopy(float(self.item(i, 0).text()))
            y_val = deepcopy(float(self.item(i, 1).text()))
            heading_val = deepcopy(float(self.item(i, 3).text()))
            track_val = deepcopy(float(self.item(i, 2).text()))
            enabled_val = deepcopy(self.item(i, 4).checkState() == Qt.Checked)
            waypoint = Waypoint(x_val, y_val, track_val, heading_val, enabled = enabled_val)
            # print(waypoint)

            self.model.waypoints[i] = waypoint
        self.model.update()

    def draw_table(self):
        self.clear()

        for wp in self.model:
            self.add_waypoint(wp)


    def get_waypoints(self):
        self.update()
        return self.waypoints


    def item_changed(self, item):
        row = item.row()
        x_val = float(self.item(row, 0).text())
        y_val = float(self.item(row, 1).text())
        track_val = float(self.item(row, 2).text())
        heading_val = float(self.item(row, 3).text())
        enabled_val = self.item(row, 4).checkState() == Qt.CheckState.Checked

        self.model[row] = Waypoint(x_val, y_val, track_val, heading_val, enabled = enabled_val)

    def dragUpdate(self, row):
        x_val = float(self.item(row, 0).text())
        y_val = float(self.item(row, 1).text())
        track_val = float(self.item(row, 2).text())
        heading_val = float(self.item(row, 3).text())
        enabled_val = self.item(row, 4).checkState() == Qt.CheckState.Checked

        self.model[row] = Waypoint(x_val, y_val, track_val, heading_val, enabled = enabled_val)

    def add_waypoint(self, wp: Waypoint, location: int=None):
        # TODO: Fix model implementation so the
        # textChanged signal can be used instead of
        # editing finished.s

        self.blockSignals(True)
        num_rows = self.rowCount()
        if location is None:
            location=num_rows

        self.insertRow(location)

        self.checkboxItem = QTableWidgetItem()
        self.checkboxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.checkboxItem.setCheckState(Qt.Checked if wp.enabled else Qt.Unchecked)
        self.delete_button = QPushButton("X")
        self.delete_button.clicked.connect(lambda: self.delete_row(location))

        self.setItem(location, 0, QTableWidgetItem(str(wp.x)))
        self.setItem(location, 1, QTableWidgetItem(str(wp.y)))
        self.setItem(location, 2, QTableWidgetItem(str(wp.track)))
        self.setItem(location, 3, QTableWidgetItem(str(wp.heading)))
        self.setItem(location, 4, self.checkboxItem)

        self.setCellWidget(location, 5, self.delete_button)

        self.blockSignals(False)

    def delete_row(self, rowNum):


        del self.model[rowNum]

        self.num_waypoints -= 1

        # tempWidget = QWidget()
        # tempWidget.setLayout(self)
        # tempWidget.deleteLater()

        # self = QGridLayout()
        # self.setAlignment(Qt.AlignTop)

        # for wp in waypoints:
        #     self.add_waypoint(wp)

        # self.setLayout(self)
        # self.update()

    def clear(self):
        self.num_waypoints = 0

        self.setRowCount(0)

        #self.setLayout(self)



class WaypointTable(QWidget):
    flipSignal = Signal()

    def __init__(self, model: WaypointModel, field: FieldView):
        super().__init__()

        self.model = model
        self.field = field

        self.setMinimumSize(1010, 300)

        self.addButton = QPushButton('Add Point')
        self.addButton.clicked.connect(lambda: self.add_waypoint())
        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.update)
        self.animateButton = QPushButton('Animate')
        self.flipButton = QPushButton('Flip Field')
        self.flipButton.clicked.connect(self.flipSignal.emit)
        self.flipButton.setEnabled(False)
        self.loadButton = QPushButton('Load Auto')
        self.loadButton.clicked.connect(self.load_auto_wp_table)
        self.saveButton = QPushButton('Save Auto')
        self.saveButton.clicked.connect(self.save_auto)
        # self.showButton = QPushButton('Show Auto')
        # self.showButton.clicked.connect(self.show_auto)
        self.gifCheckboxLabel = QLabel("Save Gif: ")
        self.gifCheckboxLabel.setMaximumWidth(60)
        self.gifCheckbox = QCheckBox()
        self.gifCheckbox.setMaximumWidth(25)
        self.howToUseButton = QPushButton('?')
        self.howToUseButton.clicked.connect(self.program_explanation)
        self.howToUseButton.setMaximumSize(32, 32)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.howToUseButton)
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.updateButton)
        self.buttonLayout.addWidget(self.animateButton)
        self.buttonLayout.addWidget(self.flipButton)
        self.buttonLayout.addWidget(self.loadButton)
        self.buttonLayout.addWidget(self.saveButton)
        self.buttonLayout.addWidget(self.gifCheckboxLabel)
        self.buttonLayout.addWidget(self.gifCheckbox)
        # self.buttonLayout.addWidget(self.showButton)


        # setting radius and border
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.tableBody = WaypointTableBody(self.model)
        self.scroll_area.setWidget(self.tableBody)
        self.updateSignal = self.tableBody.updateSignal

        self.test_layout = QHBoxLayout()
        self.path_list = Cordwainer(model)
        self.table = QTableWidget()

        self.wp_table_layout = QVBoxLayout()

        self.scroll_area.setWidget(self.tableBody)

        self.wp_table_layout.addWidget(self.scroll_area)

        self.test_layout.addWidget(self.path_list)
        self.test_layout.addLayout(self.wp_table_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.buttonLayout)

        self.main_layout.addLayout(self.test_layout)

        self.setLayout(self.main_layout)

        self.model.updated.connect(self.add_path)

        # self.path_list.list.currentItemChanged.connect(self.update_path)

    def add_path(self):
        if self.path_list.list.count() < 1:
            # item = self.path_list.list.addItem(Auto(f"path{str(self.path_list.list.count() + 1)}", self.get_waypoints()))
            self.path_list.list.add_item(self.get_waypoints())

            self.path_list.list.setCurrentRow(self.path_list.list.count() - 1)

    def update_path(self, current, previous):
        if previous is not None:
            previous.waypoints = self.get_waypoints()
            self.model.update(current.waypoints)
            # self.path_list.list.selection_changed()

    def update(self):
        self.tableBody.update()

    def get_waypoints(self):
        return self.model.waypoints

    def add_waypoint(self, wp: Waypoint=Waypoint(0, 0, 0, 0)):
        self.model.append(wp)

    def delete_row(self, rowNum):
        self.tableBody.delete_row(rowNum)

    def load_auto_wp_table(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select File to Load', '.', 'JSON File (*.json)')
        auto = load_auto(filename)
        if auto is not None:
            self.path_list.list.set_items(auto)


    def save_auto(self):
        if self.path_list.list.count() > 0:
            default_name = 'auto.json'
            last_x = None
            last_y = None
            last_heading = None

            for path in self.path_list.get_paths(): 
                if last_x is not None:
                    if last_x != path.waypoints[0].x or last_y != path.waypoints[0].y or last_heading != path.waypoints[0].heading:
                        msg = QMessageBox()
                        msg.setWindowTitle("Error!")
                        msg.setIcon(QMessageBox.Warning)
                        msg.setGeometry(500, 500, 500, 500)
                        msg.setText(f"One of your paths doesn't end with the same point that begins the subsequent path at {path.text()}")
                        msg.exec()
                last_x = path.waypoints[len(path.waypoints) - 1].x
                last_y = path.waypoints[len(path.waypoints) - 1].y
                last_heading = path.waypoints[len(path.waypoints) - 1].heading
            filename, _ = QFileDialog.getSaveFileName(self, 'Select File to Save', f'./{default_name}', 'JSON File (*.json)')


            if filename is None:
                return

            json_obj = dict()

            paths = self.path_list.get_paths()
            #json_obj['id'] = 1
            json_obj['name'] = os.path.splitext(os.path.basename(filename))[0]
            json_obj['path_count'] = len(paths)
            #json_obj['reversed'] = False

            json_obj['paths'] = []

            for i, path in enumerate(paths):
                json_obj['paths'].append({})
                json_obj["paths"][i]["name"] = path.text()
                if path.speed:
                    json_obj["paths"][i]["max_velocity"] = int(path.speed)                 
                json_obj["paths"][i]["waypoints"] = []
                for wp in path.waypoints:
                    json_obj["paths"][i]["waypoints"].append(wp.toJson())


            path_json = json.dumps(json_obj, indent=4)
            if filename != '' or filename is None or filename != "":
                with open(filename, 'w') as f:
                    f.write(path_json)
                    if self.isGifEnabled():
                        self.screenshot(filename)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("You must have at least one path in an auto!")
            msg.setIcon(QMessageBox.Warning)
            msg.setGeometry(100, 200, 100, 100)
            msg.exec()

    def program_explanation(self):
        msg = QMessageBox()
        msg.setWindowTitle("hello")
        msg.setText("This application is used to create autos for the robot. It creates 'paths' which the robot follows. These paths make up the auto that the robot follows. This program can be used to make both paths and autos. Plot points on the field or in the table, save the path, and then add those saved paths to the 'Cordwainer'(the auto maker). Once that is completed, the paths can be edited and then the paths are exported into a new auto. This auto can then be put into the robot code to be run during the Autonomous period")
        msg.setIcon(QMessageBox.Information)
        msg.setGeometry(500, 500, 500, 500)
        msg.exec()

    def isGifEnabled(self):
        if self.gifCheckbox.isChecked():
            return True
        else:
            return False

    
    def screenshot(self, filename):
        # auto = load_auto(filename.replace(".png", ".json"))
        # for file in os.scandir('./resources/animation_in'):
        #     os.remove(file.path)
        # for wp in path.waypoints:
        #         waypoints.append(wp)
        path_num = 0
        p = 0

        images = []

        for path in self.path_list.get_paths():

            path_num += 1

            waypoints = path.waypoints

            # self.model.update(waypoints)
            self.path_list.list.setCurrentItem(path)

            tiny_points = calc_splines(waypoints)

            screenshot_area = QRect(self.field.x(), self.field.y(), self.field.width() / 2, self.field.height())
            screenshot: QPixmap = self.window().grab(screenshot_area)



            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            screenshot.toImage().save(buffer, 'PNG')
            pil_img = Image.open(io.BytesIO(buffer.data()))
            # Image.open


            # screenshot.save(f"./resources/animation_in/{path.name}.png")



            skip = 0
            for pt in tiny_points:
                #Ignore this
                skip += 1
                if skip == 15:

                    skip = 0


                    # test = Image.open((f"./resources/animation_in/{path.name}.png"))
                    test = pil_img.copy()
                    image = ImageDraw.Draw(test)


                    px = (self.field.inches_to_pixels(pt.x, 0)[0] * 2)
                    py = (self.field.inches_to_pixels(0, pt.y)[1] * 2)

                    # transfrom = int(math.sin(pt.heading) * robot_size)

                    # image.regular_polygon((px , py, 75), n_sides= 4, rotation=pt.heading, fill="black", outline="red")
                    xy = ImageDraw._compute_regular_polygon_vertices((px , py, 65), 4, pt.heading)
                    image.polygon(xy, "black", "red", 10)
                    constant = 65
                    xtransform = constant*math.cos(math.radians(pt.heading))
                    ytransform = constant*math.sin(math.radians(pt.heading))
                    image.line(((px, py), (px+xtransform, py-ytransform)), fill="white", width = 5)

                    image.text((15, test.size[1] - 175), str(path_num), (237, 230, 211), font = ImageFont.truetype("Arial Unicode.ttf", 150))

                    # i = "{:03d}".format(p)
                    # output = BytesIO()
                    # test.save(output, format= "PNG")
                    # output.seek(1)
                    images.append(test)
                    p += 1
                    # images.append(test.save(f"./resources/animation_in/auto_animation_{i}.png"))

        self.make_gif(filename.replace(".json", ""), images)

        # self.make_gif(filename.replace(".json", ""), images)
        # output.flush()

    # def show_auto(self):
    #     waypoints = []
    #     auto = self.path_list.get_paths()
    #     last_item = None
    #     if auto is not None:
    #         for path in auto:
    #             if last_item is not None and last_item != path.waypoints[0].x  :
    #                 msg = QMessageBox()
    #                 msg.setWindowTitle("Error!")
    #                 msg.setIcon(QMessageBox.Warning)
    #                 msg.setGeometry(500, 500, 500, 500)
    #                 msg.setText("One of your paths doesn't end with the same point that begins the subsequent path")
    #                 msg.exec()
    #             last_item = path.waypoints[len(path.waypoints) - 1].x
    #             self.path_list.list.addItem(path)
    #             for wp in path.waypoints:
    #                 waypoints.append(wp)
    #         self.model.update(waypoints)

    def make_gif(self, file_name, files):
        images = []
        for filename in files:
            images.append(filename)
        iio.mimsave(f'{file_name}.gif', images, fps=15)
        # optimize(file_name)

