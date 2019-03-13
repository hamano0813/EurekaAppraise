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
        basic_tab.add_widget(LineEdit(100), '项目全称')
        basic_tab.add_widget(DateEdit(), '评估基准日')
        basic_tab.add_widget(LineEdit(20), '项目文号')
        basic_tab.add_widget(LineEdit(100), '评估对象')
        basic_tab.add_widget(LineEdit(100), '评估范围')
        basic_tab.add_widget(CheckCombo(['资产基础法', '收益法', '市场法']), '评估方法')
        basic_tab.add_widget(IntEdit(), '标准收费（万元）')
        basic_tab.add_widget(IntEdit(), '实际收费（万元）')
        basic_tab.add_widget(LineEdit(10), '企业填表人')
        basic_tab.add_widget(SwitchRadio(['是', '否', '不适用']), '项目备案')

        self.addTab(basic_tab, basic_tab.information_model.table_name)
