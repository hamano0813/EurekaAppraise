#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt5 import QtWidgets
from program.asset_method.work_table.detail_view import DetailView
from program.asset_method.work_table.detail_model import DetailModel
from program.asset_method.work_table.datail_delegate import DetailDelegate

if __name__ == '__main__':
    file = "C:/PyAppraiseData/2019-100.db3"
    conn = sqlite3.connect(file)
    app = QtWidgets.QApplication(sys.argv)
    view = DetailView()
    model = DetailModel(conn, '表3-1-2')
    delegate = DetailDelegate()
    view.setModel(model)
    view.setItemDelegate(delegate)
    view.show()
    sys.exit(app.exec_())
