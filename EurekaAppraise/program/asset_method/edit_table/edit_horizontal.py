#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui


class EditHorizontalHeader(QtWidgets.QHeaderView):
    def __init__(self, orient=QtCore.Qt.Horizontal, parent=None):
        QtWidgets.QHeaderView.__init__(self, orient, parent)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested[QtCore.QPoint].connect(self.header_menu)

    def header_menu(self, pos: QtCore.QPoint):
        position_idx = self.parent().indexAt(pos).column()
        menu = QtWidgets.QMenu()
        ascending_action = QtWidgets.QAction(self.tr('Ascending'), self)
        ascending_action.triggered.connect(partial(self.parent().model().sort, position_idx, True))
        menu.addAction(ascending_action)
        descending_action = QtWidgets.QAction(self.tr('Descending'), self)
        descending_action.triggered.connect(partial(self.parent().model().sort, position_idx, False))
        menu.addAction(descending_action)
        if position_idx >= 0:
            menu.exec_(QtGui.QCursor().pos())
