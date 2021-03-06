#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui


class TotalView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        self.horizontalHeader().hide()
        self.horizontalScrollBar().setStyleSheet('QScrollBar:horizontal{height:0px;}')
        self.verticalHeader().setFixedWidth(50)
        self.verticalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.verticalHeader().setHighlightSections(False)
        self.setFixedHeight(33)
        self.setWordWrap(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)

    def set_width(self, idx, old, new):
        self.setColumnWidth(idx, new)

    def key_press(self, func):
        # noinspection PyArgumentList
        def wrapper(event: QtGui.QKeyEvent):
            if event.key() == QtCore.Qt.Key_C and event.modifiers() == QtCore.Qt.ControlModifier:
                QtWidgets.QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
            else:
                func(event)

        return wrapper
