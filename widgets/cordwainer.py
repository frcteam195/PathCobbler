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
        self.clear_button = QPushButton("clear path")


        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.clear_button)


class ShoeList(QListWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        self.waypoint_model = model
        # self.waypoint_model.updated.connect(self.update_item)
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
            
        self.takeItem(items)

    def add_item(self, waypoints: List[Waypoint]=[]):
        print('add me')
        # self.currentItem().waypoints = self.waypoint_model.waypoints

        # last_item_num = int(self.item(self.count-1).name[-1])

        last_waypoint = deepcopy(self.waypoint_model.waypoints[-1])

        print(waypoints)
        if waypoints == []:
            print('empty')
            waypoints.append(last_waypoint)

        # print(waypoints)
        new_item = Auto(f"path{self.pathIndex}", waypoints)
        self.pathIndex += 1
        # self.waypoint_model.clear_model()

        self.addItem(new_item)

        self.setCurrentItem(new_item)
        
    def selection_changed(self, current, previous):
        if previous is not None:
            print(previous.waypoints)
            previous.waypoints = deepcopy(self.waypoint_model.waypoints)

        # print('current', current.waypoints)
            if len(self.waypoint_model) > 0:
                self.waypoint_model.clear_model()
            
            # print(type(current.waypoints))
            self.waypoint_model.update(current.waypoints)
        
        # if current is not None:
        #     print(current.waypoints)

        # item = self.currentItem()
        
        # print('changed')
        # if item is not None:
        #     self.waypoint_model.update(item.waypoints)
        # else:
        #     self.waypoint_model.clear_model()

    def add_paths(self, names, wps):
        self.names = names
        self.wps = wps
        
class Cordwainer(QWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        self.layout = QVBoxLayout()
        self.list = ShoeList(model)
        self.buttons = ShoeButtons()
        self.model = model

        self.buttons.setGeometry(self.buttons.x()-100, self.buttons.y(), self.buttons.width(), self.buttons.height())

        self.layout.addWidget(self.list, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.buttons, alignment=Qt.AlignRight)

        self.setLayout(self.layout)

        self.setWindowTitle("The Cordwainer")

        self.buttons.remove_button.clicked.connect(self.list.remove_item)
        self.buttons.add_button.clicked.connect(lambda: self.list.add_item([]))
        self.buttons.clear_button.clicked.connect(self.model.clear_model)
    
    def get_paths(self):
        return self.list.get_items()