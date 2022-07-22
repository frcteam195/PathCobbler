import json

from PySide6.QtWidgets import *


def open_json_file(filename):
    if filename is None or len(filename) == 0:
        return None

    path_json = None

    with open(filename, 'r') as f:
        path_json = json.loads(f.read())

    return path_json


def write_json_file(filename):
    pass
