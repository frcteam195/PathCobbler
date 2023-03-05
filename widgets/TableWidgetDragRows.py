import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TableWidgetDragRows(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent):
        delete_button_index = 3
        check_box_index = 2
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = [[QTableWidgetItem(self.item(row_index, column_index)) for column_index in range(self.columnCount())]
                            for row_index in rows]
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1
            delete_button = QPushButton("X")
            delete_button.clicked.connect(lambda: print("delete"))
            checkboxItem = QTableWidgetItem()
            checkboxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    if column_index == check_box_index:
                        self.setItem(row_index, check_box_index, checkboxItem)
                    elif column_index == delete_button_index:
                        self.setCellWidget(row_index, delete_button_index, delete_button)
                        continue

                    self.setItem(row_index, column_index, column_data)
                    print(row_index, column_index, column_data)
                
            event.accept()
            # for row_index in range(len(rows_to_move)):
            #     self.item(drop_row + row_index, 0).setSelected(True)
            #     self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)

        # for r in range(0, self.rowCount()):
        #     print(f"Current Row: {r}")
        #     for c in range(0, self.columnCount()-1):
        #         print(f"Current Column: {c}")
        #         print(f"Item: {self.item(r, c).text()}")
        #         # print(f"")

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.table_widget = TableWidgetDragRows()
        layout.addWidget(self.table_widget) 

        # setup table widget
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Type', 'Name', 'Delete'])

        items = [('Cyber', 'Squire'), ('Cyber', 'Knights'), ('19', '5'), ('I <3', 'Tyler'), ('Joe', 'sux')]
        self.table_widget.setRowCount(len(items))
        for i, (color, model) in enumerate(items):
            self.table_widget.setItem(i, 0, QTableWidgetItem(color))
            self.table_widget.setItem(i, 1, QTableWidgetItem(model))

            delete_button = QPushButton("Delete")
            checkboxItem = QTableWidgetItem()
            checkboxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            self.table_widget.setItem(i, 2, checkboxItem)
            self.table_widget.setCellWidget(i, 3, delete_button)
            delete_button.clicked.connect(lambda: print("delete"))
            #self.table_widget.cellWidget(i, 2).show()
        self.resize(400, 400)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())