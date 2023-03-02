import os
import signal

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from utils.file_utils import *
from widgets.waypoint_model import *
from utils.auto import Auto
from copy import deepcopy
# from widgets.waypoint_table import *

signal.signal(signal.SIGINT, signal.SIG_DFL)
class ShoeButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        self.setLayout(layout)

        self.add_button = QPushButton("Add Path")
        self.remove_button = QPushButton("Remove Path")
        self.clear_button = QPushButton("Clear Path")
        self.speed_textbox = QLineEdit()
        self.speed_textbox.setMaximumSize(32, 32)


        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.speed_textbox)


class ShoeList(QListWidget):
    def __init__(self, model: WaypointModel, buttons: ShoeButtons):
        super().__init__()
        self.waypoint_model = model
        self.buttons = buttons
        self.waypoint_model.updated.connect(self.update_item)
        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.setDefaultDropAction(Qt.DropAction.MoveAction)

        self.currentItemChanged.connect(self.selection_changed)

        self.pathIndex = 1

    def get_items(self):
        paths = []
        for path in range(self.count()):
            paths.append(self.item(path))
        return paths

    def remove_item(self):
        items = self.currentRow()
        if self.count() > 1:
            if self.currentRow() < self.count()-1:
                self.setCurrentRow(items+1)
            else:
                self.setCurrentRow(items-1)
        else:
            self.clearSelection()
            self.waypoint_model.clear_model()

        self.takeItem(items)

    def update_item(self):
        if self.currentItem() is not None:
            self.currentItem().waypoints = deepcopy(self.waypoint_model.waypoints)

    def add_item(self, waypoints: List[Waypoint]=[]):
        # print('add me')
        # self.currentItem().waypoints = self.waypoint_model.waypoints

        # last_item_num = int(self.item(self.count-1).name[-1])

        if len(self.waypoint_model) > 0:
            last_waypoint = deepcopy(self.waypoint_model.waypoints[-1])
            # print(last_waypoint)

            if waypoints == []:
                # print('empty')
                waypoints.append(last_waypoint)
            # print(waypoints)

        # print(waypoints)
        new_item = Auto(f"path{self.pathIndex}", waypoints)
        self.pathIndex += 1
        # self.waypoint_model.clear_model()

        self.addItem(new_item)

        self.setCurrentItem(new_item)

    def set_items(self, items: List[Auto]):
        self.clear()

        for item in items:
            self.addItem(item)
            # for wp in item.waypoints:
            #     print(wp)
            # print(' ')

        self.setCurrentRow(self.count() - 1)

        self.pathIndex = self.count() + 1


    def selection_changed(self, current, previous):
        if previous is not None:
            previous.waypoints = deepcopy(self.waypoint_model.waypoints)
            previous.speed = deepcopy(self.buttons.speed_textbox.text())

        if current is not None:
            self.waypoint_model.update(current.waypoints)
            if current.speed is not None:
                self.buttons.speed_textbox.setText(current.speed)
            else:
                self.buttons.speed_textbox.clear()

    def add_paths(self, names, wps):
        self.names = names
        self.wps = wps
    
    def add_speed(self, speed):
        self.currentItem().speed = speed



class Cordwainer(QWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        self.layout = QVBoxLayout()
        self.buttons = ShoeButtons()
        self.list = ShoeList(model, self.buttons)
        self.model = model

        self.buttons.setGeometry(self.buttons.x()-100, self.buttons.y(), self.buttons.width(), self.buttons.height())

        self.layout.addWidget(self.list, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.buttons, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle("The Cordwainer")

        self.buttons.remove_button.clicked.connect(self.list.remove_item)
        self.buttons.add_button.clicked.connect(lambda: self.list.add_item([]))
        self.buttons.clear_button.clicked.connect(self.clear_all)
        self.buttons.speed_textbox.editingFinished.connect(lambda: self.list.add_speed(self.buttons.speed_textbox.text()))

    def get_paths(self):
        return self.list.get_items()
    def clear_all(self):
        self.buttons.speed_textbox.clear()
        self.model.clear_model()
