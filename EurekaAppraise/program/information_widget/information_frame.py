#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from .information_tab import InformationTab
from ..custom_widget.table_editor import DateEdit, LineEdit, RealEdit
from ..custom_widget.information_editor import CheckCombo, SwitchRadio, TextEdit


class InformationFrame(QtWidgets.QTabWidget):
    def __init__(self, conn, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        self.conn = conn

        basic_tab = InformationTab(conn, '基础信息')
        code_line = LineEdit(8)
        code_line.setReadOnly(True)
        basic_tab.add_widget(code_line, '项目编号')
        basic_tab.add_widget(DateEdit(), '评估基准日')
        basic_tab.add_widget(LineEdit(20), '项目文号')
        basic_tab.add_widget(TextEdit(60), '项目全称')
        basic_tab.add_widget(TextEdit(50), '评估对象')
        basic_tab.add_widget(TextEdit(50), '评估范围')
        basic_tab.add_widget(CheckCombo(['资产基础法', '收益法', '市场法']), '评估方法')
        basic_tab.add_widget(RealEdit(), '标准收费（万元）')
        basic_tab.add_widget(RealEdit(), '实际收费（万元）')
        basic_tab.add_widget(LineEdit(10), '企业填表人')
        basic_tab.add_widget(SwitchRadio(['是', '否', '不适用']), '项目备案')
        self.add_tab(basic_tab)

        principal_tab = InformationTab(conn, '委托方信息')
        principal_tab.add_widget(TextEdit(50), '名称')
        principal_tab.add_widget(TextEdit(100), '住所')
        principal_tab.add_widget(DateEdit(), '成立日期')
        principal_tab.add_widget(DateEdit(), '经营期限开始')
        principal_tab.add_widget(DateEdit(), '经营期限结束')
        principal_tab.add_widget(LineEdit(20), '注册资金')
        principal_tab.add_widget(LineEdit(20), '实收资本')
        principal_tab.add_widget(TextEdit(200), '经营范围')
        principal_tab.add_widget(LineEdit(10), '联系人')
        principal_tab.add_widget(LineEdit(20), '联系电话')
        self.add_tab(principal_tab)

        occupant_tab = InformationTab(conn, '资产占有方信息')
        occupant_tab.add_widget(TextEdit(50), '名称')
        occupant_tab.add_widget(TextEdit(100), '住所')
        occupant_tab.add_widget(DateEdit(), '成立日期')
        occupant_tab.add_widget(DateEdit(), '经营期限开始')
        occupant_tab.add_widget(DateEdit(), '经营期限结束')
        occupant_tab.add_widget(LineEdit(20), '注册资金')
        occupant_tab.add_widget(LineEdit(20), '实收资本')
        occupant_tab.add_widget(TextEdit(200), '经营范围')
        occupant_tab.add_widget(LineEdit(10), '联系人')
        occupant_tab.add_widget(LineEdit(20), '联系电话')
        self.add_tab(occupant_tab)

    def add_tab(self, tab_widget: InformationTab):
        tab_widget.mapper.toFirst()
        self.addTab(tab_widget, tab_widget.information_model.table)
