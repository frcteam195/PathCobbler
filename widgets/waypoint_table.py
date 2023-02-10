import os
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from utils.waypoint import Waypoint
from widgets.path_list import PathList
from widgets.waypoint_model import WaypointModel
from widgets.field_view import FieldView
from widgets.cordwainer import Cordwainer
from utils.auto import Auto

from utils.file_utils import *

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from utils.waypoint import Waypoint
from widgets.waypoint_model import WaypointModel


class WaypointTableBody(QTableWidget):
    updateSignal = Signal(list, name='updateSignal')

    def __init__(self, model: WaypointModel):
        super().__init__()

        self.waypoints = []
        self.model = model
        self.num_waypoints = 0
        # self.resize(500, 100)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


        self.model.updated.connect(self.draw_table)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(["X", "Y", "Header", "Enabled", "Delete"])

        self.itemChanged.connect(self.item_changed)

    def update(self):

        waypoints = []

        for i in range(1, self.rowCount()):
            x_val = float(self.item(i, 0))
            y_val = float(self.item(i, 1))
            heading_val = float(self.item(i, 1))
            enabled_val = float(self.item(i, 1))

            waypoints.append(Waypoint(x_val, y_val, heading_val, enabled=enabled_val))

        self.model.update(waypoints)

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
        heading_val = float(self.item(row, 2).text())
        enabled_val = self.item(row, 3).checkState() == Qt.CheckState.Checked

        self.model[row] = Waypoint(x_val, y_val, heading_val, enabled = enabled_val)
        print(x_val, y_val, heading_val, enabled_val)

    def add_waypoint(self, wp: Waypoint):
        # TODO: Fix model implementation so the
        # textChanged signal can be used instead of
        # editing finished.s

        self.blockSignals(True)
        num_rows = self.rowCount()

        self.insertRow(num_rows)

        self.checkboxItem = QTableWidgetItem()
        self.checkboxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.checkboxItem.setCheckState(Qt.Checked if wp.enabled else Qt.Unchecked)
        self.delete_button = QPushButton("X")
        self.delete_button.clicked.connect(lambda: self.delete_row(num_rows ))

        x_input = QTableWidgetItem(str(wp.x))

        y_input = QTableWidgetItem(str(wp.y))

        heading_input = QTableWidgetItem(str(wp.heading))


        self.setItem(num_rows, 0, x_input)
        self.setItem(num_rows, 1, QTableWidgetItem(str(wp.y)))
        self.setItem(num_rows, 2, QTableWidgetItem(str(wp.heading)))
        self.setItem(num_rows, 3, self.checkboxItem)

        self.setCellWidget(num_rows, 4, self.delete_button)

        self.blockSignals(False)

    def delete_row(self, rowNum):

        print(rowNum)

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

        self.setMinimumSize(920, 300)

        self.addButton = QPushButton('Add Point')
        self.addButton.clicked.connect(lambda: self.add_waypoint())
        self.updateButton = QPushButton('Update')
        self.updateButton.clicked.connect(self.update)
        self.animateButton = QPushButton('Animate')
        self.flipButton = QPushButton('Flip Field')
        self.flipButton.clicked.connect(self.flipSignal.emit)
        self.loadButton = QPushButton('Load Auto')
        self.loadButton.clicked.connect(self.load_path)
        self.saveButton = QPushButton('Save Auto')
        self.saveButton.clicked.connect(self.save_auto)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.addButton)
        self.buttonLayout.addWidget(self.updateButton)
        self.buttonLayout.addWidget(self.animateButton)
        self.buttonLayout.addWidget(self.flipButton)
        self.buttonLayout.addWidget(self.loadButton)
        self.buttonLayout.addWidget(self.saveButton)



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

    def update(self):
        self.tableBody.update()

    def get_waypoints(self):
        return self.model.waypoints

    def add_waypoint(self, wp: Waypoint=Waypoint(0, 0, 0)):
        self.model.append(wp)
        pass
    def delete_row(self, rowNum):
        self.tableBody.delete_row(rowNum)

    def load_path(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select File to Load', '.', 'JSON File (*.json)')
        waypoints = []
        auto = load_auto(filename)
        if auto is not None:
            for path in auto:
                self.path_list.list.addItem(path)
                for wp in path.waypoints:
                    waypoints.append(wp)
        self.model.update(waypoints)



    def save_auto(self):
        if self.path_list.list.count() > 0:
            default_name = 'auto.json'
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
        else:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("You must have at least one path in an auto!")
            msg.setIcon(QMessageBox.Warning)
            msg.setGeometry(100, 200, 100, 100)
            msg.exec()

    def screenshot(self, filename):
        screenshot_area = QRect(self.field.x(), self.field.y(), self.field.width(), self.field.height())
        screenshot = self.window().grab(screenshot_area)
        screenshot.save(filename)