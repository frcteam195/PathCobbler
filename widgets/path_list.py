from typing import List

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from utils.path import Path
from widgets.path_model import PathModel


class PathList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.paths = []

        self.paths.append(Path('Path1'))
        self.paths.append(Path('Path2'))

        self.model = PathModel(self.paths)

        self.pathView = QListView()
        self.pathView.setModel(self.model)
        self.pathView.setCurrentIndex(self.model.index(0, 0))

        layout.addWidget(self.pathView)

        self.setLayout(layout)
