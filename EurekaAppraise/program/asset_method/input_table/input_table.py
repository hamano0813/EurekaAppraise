#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtWidgets, QtCore
from .input_model import InputModel
from .input_delegate import InputDelegate
from .input_view import InputView


class InputTable(QtWidgets.QFrame):
    # noinspection PyArgumentList
    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        QtWidgets.QFrame.__init__(self, parent, flags=QtCore.Qt.WindowCloseButtonHint)

        self.edt_v = InputView()
        self.edt_m = InputModel(conn, table_name)
        self.edt_d = InputDelegate()
        self.edt_v.setModel(self.edt_m)
        self.edt_v.setItemDelegate(self.edt_d)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setSpacing(2)
        main_layout.addWidget(self.edt_v, 0, 0, 1, 1)
        self.setLayout(main_layout)
