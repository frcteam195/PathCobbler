import os
import sys
import time
import signal

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from utils.file_utils import *
from widgets.waypoint_model import *

signal.signal(signal.SIGINT, signal.SIG_DFL)


class Auto(QListWidgetItem):
    def __init__(self, name, waypoints):
        super().__init__(name)
        self.name = name
        self.waypoints = waypoints



class ShoeButtons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()

        layout.setAlignment(Qt.AlignRight)

        self.setLayout(layout)

        self.add_button = QPushButton("Add")
        self.remove_button = QPushButton("Remove")

        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)   

class ShoeList(QListWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        #layout = QGridLayout()
        #self.setLayout(layout)
        #self = QListWidget()
        self.model = model

        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        
        #layout.addWidget(self)

        self.currentItemChanged.connect(self.selection_changed)
    
    def remove_item(self):
        items = self.currentRow()
        self.takeItem(items)      

    def add_item(self):
        self.dialog = QFileDialog()
        self.fileName, _ = self.dialog.getOpenFileName(self, 'Open file', 
        '.',"Json files (*.json)")
        
        # new_item = QListWidgetItem(os.path.splitext(os.path.basename(self.fileName))[0])
        new_item = Auto(os.path.splitext(os.path.basename(self.fileName))[0], load_path(self.fileName))

        self.model.update(new_item.waypoints)

        self.addItem(new_item)

        self.setCurrentItem(new_item)

    def selection_changed(self):
        item = self.currentItem()
        self.model.update(item.waypoints)

class Cordwainer(QWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        self.layout = QVBoxLayout()
        self.list = ShoeList(model)
        self.buttons = ShoeButtons()
        self.model = model


        self.layout.addWidget(self.list, alignment=Qt.AlignRight)
        self.layout.addWidget(self.buttons, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)

        self.setWindowTitle("The Cordwainer")

        self.buttons.remove_button.clicked.connect(self.list.remove_item)
        self.buttons.add_button.clicked.connect(self.list.add_item)