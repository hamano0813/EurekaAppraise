#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from .information_model import InformationModel


class InformationFrame(QtWidgets.QFrame):
    def __init__(self, conn, table_name, parent, flags):
        QtWidgets.QFrame.__init__(self, parent, flags)
        self.conn = conn
        self.table_name = table_name
        self.mapper = QtWidgets.QDataWidgetMapper()
        self.information_model = InformationModel(self.conn, table_name, flags)
        self.main_layout = QtWidgets.QGridLayout()

    def add_widget(self, editor: QtWidgets.QWidget, field_cid: int, layout: list):
        name = self.information_model.title_name[field_cid]
        label = QtWidgets.QLabel(name, self)
        editor_layout = layout.copy()
        editor_layout[1] = layout[1] * 2 + 1
        self.main_layout.addWidget(label, *layout)
        self.main_layout.addWidget(editor, *editor_layout)
        self.mapper.addMapping(editor, field_cid)
