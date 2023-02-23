import json

from utils.waypoint import Waypoint

from PySide6.QtWidgets import *
from utils.auto import Auto

def open_json_file(filename):
    if filename is None or len(filename) == 0:
        return None

    path_json = None

    with open(filename, 'r') as f:
        path_json = json.loads(f.read())

    return path_json


def write_json_file(filename):
    pass

def load_path(filename):
    path_json = open_json_file(filename)

    if path_json is None:
        return None

    # self.tableBody.clear()
    waypoints = []
    if 'waypoints' in path_json:
        for wp_json in path_json['waypoints']:
            waypoints.append(Waypoint(wp_json['x'], wp_json['y'], wp_json['track'], wp_json['heading']))
        return waypoints
    else:
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("You need a valid path!")
        msg.setIcon(QMessageBox.Warning)
        msg.setGeometry(100, 200, 100, 100)
        msg.exec()
        return None

def load_auto(filename):
    path_json = open_json_file(filename)

    if path_json is None:
        return ('', None)

    name = path_json['name']

    paths = []
    if 'paths' in path_json:
        for path in path_json['paths']:
            waypoints = []
            for wp in path['waypoints']:
                waypoints.append(Waypoint(wp['x'], wp['y'], wp['track'], wp['heading']))

            paths.append(Auto(path['name'], waypoints))
        return (name, paths)
    else:
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("You need to upload a valid auto!")
        msg.setIcon(QMessageBox.Warning)
        msg.setGeometry(100, 200, 100, 100)
        msg.exec()
        return ('', None)


