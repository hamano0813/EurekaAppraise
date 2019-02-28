#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets, QtCore
from .summary_model import SummaryModel
from .summary_view import SummaryView


class SummaryTable(QtWidgets.QFrame):
    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        QtWidgets.QFrame.__init__(self, parent, flags=QtCore.Qt.WindowCloseButtonHint)
        self.sum_v = SummaryView()
        self.sum_m = SummaryModel(conn, table_name)
        self.sum_v.setModel(self.sum_m)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(3)
        # noinspection PyArgumentList
        main_layout.addWidget(self.sum_v, 0, 0, 1, 1)
        self.setLayout(main_layout)
