#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from .information_tab import InformationTab
from ..custom_widget.table_editor import DateEdit, LineEdit, IntEdit
from ..custom_widget.information_editor import CheckCombo, SwitchRadio


class InformationFrame(QtWidgets.QTabWidget):
    def __init__(self, conn, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.conn = conn

        basic_tab = InformationTab(conn, '基础信息')
        basic_tab.add_widget(LineEdit(None, 100), 3)
        basic_tab.add_widget(DateEdit(None), 1)
        basic_tab.add_widget(LineEdit(None, 20), 2)
        basic_tab.add_widget(LineEdit(None, 200), 4)
        basic_tab.add_widget(LineEdit(None, 200), 5)
        basic_tab.add_widget(LineEdit(None, 20), 6)
        basic_tab.add_widget(IntEdit(None), 7)
        basic_tab.add_widget(IntEdit(None), 8)
        basic_tab.add_widget(LineEdit(None, 10), 9)
        basic_tab.add_widget(SwitchRadio(['是', '否', '不适用']), 10)

        self.addTab(basic_tab, '基础信息')
