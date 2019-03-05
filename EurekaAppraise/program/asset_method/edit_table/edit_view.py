#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui
from .edit_vertical import EditVerticalHeader
from .edit_horizontal import EditHorizontalHeader
from .edit_model import EditModel

CHARACTER_WIDTH = 15
ROW_HEIGHT = 25


class EditView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        self.setModel = self.set_width(self.setModel)
        self.setVerticalHeader(EditVerticalHeader(QtCore.Qt.Vertical, self))
        self.setHorizontalHeader(EditHorizontalHeader(QtCore.Qt.Horizontal, self))
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows | QtWidgets.QTableView.SelectColumns)
        self.verticalHeader().setSectionsClickable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setWordWrap(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu)

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

    def delete_range(self):
        self.model().delete_range(self.selectedIndexes())
        self.reset()

    def copy_range(self):
        # noinspection PyArgumentList
        QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
        self.reset()

    def paste_range(self):
        # noinspection PyArgumentList
        self.model().paste_range(self.selectedIndexes(), QtWidgets.QApplication.clipboard().text())
        self.reset()

    def cut_range(self):
        self.copy_range()
        self.delete_range()
        self.reset()

    def key_press(self, func):
        def wrapper(event: QtGui.QKeyEvent):
            if event.key() == QtCore.Qt.Key_Delete:
                self.delete_range()
            elif event.key() == QtCore.Qt.Key_V and event.modifiers() == QtCore.Qt.ControlModifier:
                self.paste_range()
            elif event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
                self.copy_range()
            elif event.key() == QtCore.Qt.Key_X and event.modifiers() == QtCore.Qt.ControlModifier:
                self.cut_range()
            else:
                func(event)

        return wrapper

    # noinspection PyArgumentList
    def context_menu(self, pos: QtCore.QPoint):
        position_idx = self.indexAt(pos)
        self.selectedIndexes()
        menu = QtWidgets.QMenu()
        copy_action = QtWidgets.QAction(self.tr('Copy'), self)
        copy_action.triggered.connect(self.copy_range)
        menu.addAction(copy_action)
        cut_action = QtWidgets.QAction(self.tr('Cut'), self)
        cut_action.triggered.connect(self.cut_range)
        menu.addAction(cut_action)
        paste_action = QtWidgets.QAction(self.tr('Paste'), self)
        paste_action.triggered.connect(self.paste_range)
        menu.addAction(paste_action)
        delete_action = QtWidgets.QAction(self.tr('Clear'), self)
        delete_action.triggered.connect(self.delete_range)
        menu.addAction(delete_action)
        if position_idx.row() >= 0 and position_idx.column() >= 0 and position_idx.row() != self.model().rowCount() - 1:
            menu.exec_(QtGui.QCursor().pos())
