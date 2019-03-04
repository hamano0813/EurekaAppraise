#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from .edit_vertical import EditVerticalHeader
from .edit_model import EditModel

CHARACTER_WIDTH = 15
ROW_HEIGHT = 25


class EditView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        self.setModel = self.set_width(self.setModel)
        self.setVerticalHeader(EditVerticalHeader(QtCore.Qt.Vertical, self))
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows | QtWidgets.QTableView.SelectColumns)
        self.verticalHeader().setSectionsClickable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setWordWrap(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)
        self.setSortingEnabled(True)

    def set_width(self, func):
        def wrapper(model: EditModel):
            func(model)
            for idx, data_type in enumerate(model.data_type):
                title_width = len(model.title_name[idx]) * CHARACTER_WIDTH
                if data_type == 'Date':
                    self.setColumnWidth(idx, max(100, title_width))
                elif data_type == 'Real':
                    self.setColumnWidth(idx, max(120, title_width))
                elif data_type == 'Rate':
                    self.setColumnWidth(idx, max(80, title_width))
                elif data_type == 'Int':
                    self.setColumnWidth(idx, max(80, title_width))
                elif data_type == 'Percent':
                    self.setColumnWidth(idx, max(70, title_width))
                elif data_type == 'Bool':
                    self.setColumnWidth(idx, max(30, title_width))
                elif data_type.split('(')[0] == 'Nchar':
                    self.setColumnWidth(idx, max(int(data_type.split('(')[1].rstrip(')')) * 5, title_width))
            self.reset_height()
            model.rowsInserted.connect(self.reset_height)

        return wrapper

    def reset_height(self):
        for idx in range(self.model().rowCount()):
            self.setRowHeight(idx, ROW_HEIGHT)

    def key_press(self, func):
        # noinspection PyArgumentList
        def wrapper(event: QtGui.QKeyEvent):
            if event.key() == QtCore.Qt.Key_Delete:
                self.model().delete_range(self.selectedIndexes())
                self.reset()
            elif event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                self.model().paste_range(self.selectedIndexes(), QtWidgets.QApplication.clipboard().text())
                self.reset()
            elif event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
                QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
            elif event.key() == QtCore.Qt.Key_X and event.modifiers() == QtCore.Qt.ControlModifier:
                QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
                self.model().delete_range(self.selectedIndexes())
                self.reset()
            else:
                func(event)

        return wrapper
