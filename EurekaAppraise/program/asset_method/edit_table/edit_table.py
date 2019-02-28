#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui
from .edit_model import EditModel
from .edit_delegate import EditDelegate
from .edit_view import EditView
from .total_model import TotalModel
from .total_view import TotalView


class EditTable(QtWidgets.QFrame):
    # noinspection PyArgumentList
    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        QtWidgets.QFrame.__init__(self, parent, flags=QtCore.Qt.WindowCloseButtonHint)

        self.edt_v = EditView()
        self.edt_m = EditModel(conn, table_name)
        self.edt_d = EditDelegate()
        self.edt_v.setModel(self.edt_m)
        self.edt_v.setItemDelegate(self.edt_d)

        self.tot_v = TotalView()
        self.tot_m = TotalModel()
        self.tot_m.set_total(self.edt_m.total)
        self.tot_v.setModel(self.tot_m)
        [self.tot_v.setColumnWidth(idx, self.edt_v.columnWidth(idx)) for idx in range(self.edt_m.columnCount())]
        self.tot_v.horizontalScrollBar().setRange(0, self.edt_v.horizontalScrollBar().maximum())

        self.edt_v.horizontalHeader().sectionResized[int, int, int].connect(self.tot_v.set_width)
        self.edt_m.totalChanged[list].connect(self.tot_m.set_total)
        self.edt_m.totalChanged.connect(self.tot_v.reset)
        self.edt_v.horizontalScrollBar().rangeChanged[int, int].connect(self.tot_v.horizontalScrollBar().setRange)
        self.edt_v.horizontalScrollBar().valueChanged[int].connect(self.tot_v.horizontalScrollBar().setValue)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(2)
        main_layout.addWidget(self.edt_v, 0, 0, 1, 1)
        main_layout.addWidget(self.tot_v, 1, 0, 1, 1)
        self.setLayout(main_layout)

    def create_action(self, name: str, slot: classmethod = None, icon: str = None) -> QtWidgets.QAction:
        action = QtWidgets.QAction(name, self)
        action.setObjectName(name)
        if slot:
            action.triggered.connect(slot)
        if icon:
            action.setIcon(QtGui.QIcon(icon))
        return action
