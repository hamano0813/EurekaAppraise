#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from PyQt5 import QtWidgets, QtCore, QtGui


class EditVerticalHeader(QtWidgets.QHeaderView):
    def __init__(self, orient=QtCore.Qt.Vertical, parent=None):
        QtWidgets.QHeaderView.__init__(self, orient, parent)
        self.setFixedWidth(50)
        self.setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested[QtCore.QPoint].connect(self.header_menu)

    def header_menu(self, pos: QtCore.QPoint):
        position_idx = self.parent().indexAt(pos).row()
        menu = QtWidgets.QMenu()
        insert_action = QtWidgets.QAction(self.tr('Insert'), self)
        insert_action.triggered.connect(partial(self.parent().model().insertRows, position_idx, 1))
        menu.addAction(insert_action)
        if self.parent().model().rowCount() - position_idx - 1:
            remove_action = QtWidgets.QAction(self.tr('Remove'), self)
            remove_action.triggered.connect(partial(self.parent().model().removeRows, position_idx, 1))
            menu.addAction(remove_action)
        if position_idx >= 0:
            menu.exec_(QtGui.QCursor().pos())
