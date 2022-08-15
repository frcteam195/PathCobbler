import os
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel
from widgets.waypoint_table_body import WaypointTableBody

from utils.file_utils import *


class WaypointTable(QWidget):
    flipSignal = Signal()

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.model = model

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

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.buttonLayout)
        self.main_layout.addLayout(self.heading_layout)
        self.main_layout.addWidget(self.scroll_area)

        self.setLayout(self.main_layout)

    def update(self):
        self.tableBody.update()

    def get_waypoints(self) -> list[Waypoint]:
        return self.tableBody.get_waypoints()

    def add_waypoint(self, wp: Waypoint=Waypoint(0, 0, 0)):
        self.tableBody.add_waypoint(wp)

    def delete_row(self, rowNum):
        self.tableBody.delete_row(rowNum)

    def load_path(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select File to Load', '.', 'JSON File (*.json)')

        path_json = open_json_file(filename)

        if path_json is None:
            return

        # self.tableBody.clear()
        self.model.waypoints = []

        for wp_json in path_json['waypoints']:
            self.model.append(Waypoint(wp_json['x'], wp_json['y'], wp_json['theta']))

    def save_path(self):
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
