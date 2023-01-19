from typing import List

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from utils.path import Path


class PathModel(QAbstractListModel):
    def __init__(self, paths: List[Path]=None):
        super(PathModel, self).__init__()
        self.paths: List[Path] = paths or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.paths[index.row()].name

    def rowCount(self, index):
        return len(self.paths)


