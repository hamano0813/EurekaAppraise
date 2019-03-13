#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from .information_model import InformationModel
from .information_delegate import InformationDelegate


class InformationTab(QtWidgets.QScrollArea):
    def __init__(self, conn, table_name, parent=None):
        QtWidgets.QScrollArea.__init__(self, parent)
        self.area = QtWidgets.QWidget(flags=QtCore.Qt.Widget)
        self.area.setMinimumWidth(1000)
        self.height = 0
        self.mapper = QtWidgets.QDataWidgetMapper()
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.AutoSubmit)
        self.information_model = InformationModel(conn, table_name, self)
        self.mapper.setModel(self.information_model)
        self.main_layout = QtWidgets.QFormLayout(self)
        self.main_layout.setSpacing(5)
        self.area.setLayout(self.main_layout)
        self.setWidget(self.area)

    # noinspection PyArgumentList
    def add_widget(self, editor: QtWidgets.QWidget, field_name: str):
        if field_name not in self.information_model.title_name:
            return
        idx = self.information_model.title_name.index(field_name)
        self.main_layout.addRow(field_name, editor)
        self.mapper.addMapping(editor, idx)
        self.mapper.setItemDelegate(InformationDelegate())
        self.height += editor.minimumHeight() + 7
        self.area.setMinimumHeight(self.height)

    def closeEvent(self, *args, **kwargs):
        if self.information_model.conn:
            self.information_model.conn.commit()
