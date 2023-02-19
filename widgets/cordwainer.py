import os
import signal

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from utils.file_utils import *
from widgets.waypoint_model import *
from utils.auto import Auto
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
        self.save_button = QPushButton("Save Path")

        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)  
        layout.addWidget(self.save_button)


class ShoeList(QListWidget):
    def __init__(self, model: WaypointModel):
        super().__init__()
        self.model = model
        self.setDragDropMode(QAbstractItemView.DragDrop)

        self.setDefaultDropAction(Qt.DropAction.MoveAction)        

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

    def add_item(self):
        self.dialog = QFileDialog()
        self.fileName, _ = self.dialog.getOpenFileName(self, 'Open file', 
        '.',"Json files (*.json)")
        if load_path is not None:
            new_item = Auto(os.path.splitext(os.path.basename(self.fileName))[0], load_path(self.fileName))

            if self.fileName == "":
                new_item = Auto(f"path{self.count() + 1}", None)

            self.addItem(new_item)

            self.setCurrentItem(new_item)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("You need to upload a valid path!")
            msg.setIcon(QMessageBox.Warning)
            msg.setGeometry(100, 200, 100, 100)
            msg.exec()

    def selection_changed(self):
        item = self.currentItem()
        
        if item is not None:
            self.model.update(item.waypoints)
        else:
            self.model.clear_model()

    def add_paths(self, names, wps):
        self.names = names
        self.wps = wps

    def save_path(self):
        if len(self.model.waypoints) > 0:
            default_name = 'path.json'
            filename, _ = QFileDialog.getSaveFileName(self, 'Select File to Save', f'./{default_name}', 'JSON File (*.json)')
            if filename is None:
                return
            json_obj = dict()
            json_obj['id'] = 1
            json_obj['name'] = os.path.splitext(os.path.basename(filename))[0]
            json_obj['reversed'] = False
            json_obj['waypoints'] = []
            for wp in self.model:
                json_obj['waypoints'].append(wp.toJson())
            path_json = json.dumps(json_obj, indent=4)
            with open(filename, 'w') as f:
                f.write(path_json)
        else:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("You must have at least one point in a path!")
            msg.setIcon(QMessageBox.Warning)
            msg.setGeometry(100, 200, 100, 100)
            msg.exec()
        

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
        self.buttons.add_button.clicked.connect(self.list.add_item)
        self.buttons.save_button.clicked.connect(self.list.save_path)
    
    def get_paths(self):
        return self.list.get_items()