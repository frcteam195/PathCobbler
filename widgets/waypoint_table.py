import os
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from utils.waypoint import Waypoint
from widgets.path_list import PathList
from widgets.waypoint_model import WaypointModel
from widgets.waypoint_table_body import WaypointTableBody
from widgets.field_view import FieldView
from widgets.cordwainer import Cordwainer
from utils.auto import Auto

from utils.file_utils import *


class WaypointTable(QWidget):
    flipSignal = Signal()

    def __init__(self, model: WaypointModel, field: FieldView):
        super().__init__()

        self.model = model
        self.field = field

        self.setMinimumSize(500, 300)

        self.addButton = QPushButton('Add Point')
        self.addButton.clicked.connect(lambda: self.add_waypoint())
        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.update)
        self.animateButton = QPushButton('Animate')
        self.flipButton = QPushButton('Flip Field')
        self.flipButton.clicked.connect(self.flipSignal.emit)
        self.loadButton = QPushButton('Load Path')
        self.loadButton.clicked.connect(self.load_path)
        self.saveButton = QPushButton('Save Path')
        self.saveButton.clicked.connect(self.save_path)
       
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.updateButton)
        self.buttonLayout.addWidget(self.animateButton)
        self.buttonLayout.addWidget(self.flipButton)
        self.buttonLayout.addWidget(self.loadButton)
        self.buttonLayout.addWidget(self.saveButton)

        self.heading_layout = QHBoxLayout()
        x_label = QLabel('X')
        x_label.setAlignment(Qt.AlignCenter)
        y_label = QLabel('Y')
        y_label.setAlignment(Qt.AlignCenter)
        heading_label = QLabel('Heading')
        heading_label.setAlignment(Qt.AlignCenter)
        enabled_label = QLabel('Enabled')
        enabled_label.setAlignment(Qt.AlignCenter)
        delete_label = QLabel('Delete')
        delete_label.setAlignment(Qt.AlignCenter)

        self.heading_layout.addWidget(x_label)
        self.heading_layout.addWidget(y_label)
        self.heading_layout.addWidget(heading_label)
        self.heading_layout.addWidget(enabled_label)
        self.heading_layout.addWidget(delete_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.tableBody = WaypointTableBody(self.model)
        self.scroll_area.setWidget(self.tableBody)
        self.updateSignal = self.tableBody.updateSignal

        self.test_layout = QHBoxLayout()
        self.path_list = Cordwainer(model)


        self.wp_table_layout = QVBoxLayout()
        self.wp_table_layout.addLayout(self.heading_layout)
        self.wp_table_layout.addWidget(self.scroll_area)

        self.test_layout.addWidget(self.path_list)
        self.test_layout.addLayout(self.wp_table_layout)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.buttonLayout)
        # self.main_layout.addLayout(self.heading_layout)
        self.main_layout.addLayout(self.test_layout)

        self.setLayout(self.main_layout)

    def update(self):
        self.tableBody.update()

    def get_waypoints(self):
        return self.model.waypoints

    def add_waypoint(self, wp: Waypoint=Waypoint(0, 0, 0)):
        self.model.append(wp)

    def delete_row(self, rowNum):
        self.tableBody.delete_row(rowNum)

    def load_path(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select File to Load', '.', 'JSON File (*.json)')
        waypoints = []
        for path in load_auto(filename):
            self.path_list.list.addItem(path.name)
            for wp in path.waypoints:
                waypoints.append(wp)
        self.model.update(waypoints)
        

    def save_path(self):
        default_name = 'path.json'
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
            json_obj["paths"][i]["name"] = path.name
            json_obj["paths"][i]["waypoints"] = []
            for wp in path.waypoints:
                json_obj["paths"][i]["waypoints"].append(wp.toJson()) 
                

        path_json = json.dumps(json_obj, indent=4)

        with open(filename, 'w') as f:
            f.write(path_json)

        self.screenshot(filename.replace(".json", ".png"))

    def screenshot(self, filename):
        screenshot_area = QRect(self.field.x(), self.field.y(), self.field.width(), self.field.height())
        screenshot = self.window().grab(screenshot_area)
        screenshot.save(filename)