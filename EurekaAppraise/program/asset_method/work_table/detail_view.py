#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from .detail_vertical import DetailVerticalHeader
from .detail_model import DetailModel


class DetailView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super(DetailView, self).__init__(parent)
        self.setModel = self.set_width(self.setModel)
        self.setVerticalHeader(DetailVerticalHeader(QtCore.Qt.Vertical, self))
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows | QtWidgets.QTableView.SelectColumns)
        self.horizontalHeader().setHighlightSections(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)

    def set_width(self, func):
        def wrapper(model: DetailModel):
            func(model)
            for idx, data_type in enumerate(model.data_type):
                if data_type == 'Date':
                    self.setColumnWidth(idx, max(100, len(model.title_name[idx]) * 15))
                elif data_type == 'Real':
                    self.setColumnWidth(idx, max(120, len(model.title_name[idx]) * 15))
                elif data_type == 'Rate':
                    self.setColumnWidth(idx, max(80, len(model.title_name[idx]) * 15))
                elif data_type == 'Int':
                    self.setColumnWidth(idx, max(80, len(model.title_name[idx]) * 15))
                elif data_type == 'Percent':
                    self.setColumnWidth(idx, max(60, len(model.title_name[idx]) * 15))
                elif data_type == 'Bool':
                    self.setColumnWidth(idx, max(40, len(model.title_name[idx]) * 15))
                elif data_type.split('(')[0] == 'Nchar':
                    self.setColumnWidth(idx, int(data_type.split('(')[1].rstrip(')')) * 5)
            self.reset_height()
            model.rowsInserted.connect(self.reset_height)
        return wrapper

    def reset_height(self):
        for idx in range(self.model().rowCount()):
            self.setRowHeight(idx, 20)

    def key_press(self, func):
        # noinspection PyArgumentList
        def wrapper(event: QtGui.QKeyEvent):
            if event.key() == QtCore.Qt.Key_Delete:
                [self.model().setData(index, None, QtCore.Qt.EditRole)
                 for index in self.selectedIndexes()[::-1] if index.row() != self.model().rowCount()]
                self.reset()
            elif event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                self.model().paste_range(self.selectedIndexes(), QtWidgets.QApplication.clipboard().text())
                self.reset()
            elif event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
                QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
            elif event.key() == QtCore.Qt.Key_X and event.modifiers() == QtCore.Qt.ControlModifier:
                QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
                [self.model().setData(idx, None) for idx in self.selectedIndexes()]
            else:
                func(event)
        return wrapper
