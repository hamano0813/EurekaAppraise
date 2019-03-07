#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from .summary_model import SummaryModel

CHARACTER_WIDTH = 15
ROW_HEIGHT = 25


class SummaryView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        self.setModel = self.set_width(self.setModel)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows | QtWidgets.QTableView.SelectColumns)
        self.verticalHeader().setFixedWidth(50)
        self.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.verticalHeader().setSectionsClickable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setWordWrap(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested[QtCore.QPoint].connect(self.context_menu)

    def set_width(self, func):
        def wrapper(model: SummaryModel):
            func(model)
            for idx, data_type in enumerate(model.data_type):
                title_width = len(model.title_name[idx]) * CHARACTER_WIDTH
                if data_type == 'Real':
                    self.setColumnWidth(idx, max(120, title_width))
                elif data_type == 'Percent':
                    self.setColumnWidth(idx, max(70, title_width))
                elif data_type.startswith('Nchar'):
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
            if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
                self.copy_range()
            else:
                func(event)

        return wrapper

    def copy_range(self):
        # noinspection PyArgumentList
        QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))

    # noinspection PyArgumentList
    def context_menu(self, pos: QtCore.QPoint):
        position_idx = self.indexAt(pos)
        menu = QtWidgets.QMenu()
        copy_action = QtWidgets.QAction(self.tr('Copy'), self)
        copy_action.triggered.connect(self.copy_range)
        menu.addAction(copy_action)
        if position_idx.row() >= 0 and position_idx.column() >= 0:
            menu.exec_(QtGui.QCursor().pos())
