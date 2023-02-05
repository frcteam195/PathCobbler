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
        return

    # self.tableBody.clear()
    waypoints = []

    for wp_json in path_json['waypoints']:
        waypoints.append(Waypoint(wp_json['x'], wp_json['y'], wp_json['theta']))

    return waypoints

def load_auto(filename):
    path_json = open_json_file(filename)

    if path_json is None:
        return

    paths = []
    for path in path_json['paths']:
        waypoints = []
        for wp in path['waypoints']:
            waypoints.append(Waypoint(wp['x'], wp['y'], wp['theta']))

        paths.append(Auto(path['name'], waypoints))
    return paths

