#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from .information_tab import InformationTab
from ..custom_widget.table_editor import DateEdit, LineEdit


class InformationFrame(QtWidgets.QTabWidget):
    def __init__(self, conn, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.conn = conn

        basic_tab = InformationTab(conn, '基础信息')
        basic_tab.add_widget(LineEdit(None, 10), 0)
        basic_tab.add_widget(DateEdit(), 1)
        basic_tab.add_widget(LineEdit(None, 20), 2)
        basic_tab.add_widget(LineEdit(None, 100), 3)

        self.addTab(basic_tab, '基础信息')
