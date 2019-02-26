#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets, QtCore
from .detail_model import DetailModel
from .datail_delegate import DetailDelegate
from .detail_view import DetailView
from .total_model import TotalModel
from .total_view import TotalView


class WorkTable(QtWidgets.QFrame):
    # noinspection PyArgumentList
    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        super(WorkTable, self).__init__(parent, flags=QtCore.Qt.WindowCloseButtonHint)
        self.dtl_v = DetailView()
        self.dtl_m = DetailModel(conn, table_name)
        self.dtl_d = DetailDelegate()
        self.dtl_v.setModel(self.dtl_m)
        self.dtl_v.setItemDelegate(self.dtl_d)

        self.tot_v = TotalView()
        self.tot_m = TotalModel()
        self.tot_m.set_total(self.dtl_m.total)
        self.tot_v.setModel(self.tot_m)
        [self.tot_v.setColumnWidth(idx, self.dtl_v.columnWidth(idx)) for idx in range(self.dtl_m.columnCount())]
        self.dtl_v.horizontalHeader().sectionResized[int, int, int].connect(self.tot_v.set_width)
        self.tot_v.horizontalScrollBar().setRange(0, self.dtl_v.horizontalScrollBar().maximum())

        self.dtl_m.totalChanged.connect(self.tot_m.set_total)
        self.dtl_m.totalChanged.connect(self.tot_v.reset)
        self.dtl_m.detailChanged[bool].connect(self.set_unsaved)
        self.dtl_v.horizontalScrollBar().rangeChanged[int, int].connect(self.tot_v.horizontalScrollBar().setRange)
        self.dtl_v.horizontalScrollBar().valueChanged[int].connect(self.tot_v.horizontalScrollBar().setValue)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(3)
        main_layout.addWidget(self.dtl_v, 0, 0, 1, 1)
        main_layout.addWidget(self.tot_v, 1, 0, 1, 1)
        self.setLayout(main_layout)
