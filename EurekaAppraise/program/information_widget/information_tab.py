#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from .information_model import InformationModel
from .information_delegate import InformationDelegate


class InformationTab(QtWidgets.QFrame):
    def __init__(self, conn, table_name, parent=None, flags=QtCore.Qt.FramelessWindowHint):
        QtWidgets.QFrame.__init__(self, parent, flags)
        self.setWindowTitle(table_name)
        self.mapper = QtWidgets.QDataWidgetMapper()
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.AutoSubmit)
        self.information_model = InformationModel(conn, table_name, self)
        self.mapper.setModel(self.information_model)
        self.main_layout = QtWidgets.QFormLayout()
        self.main_layout.setSpacing(5)
        self.setLayout(self.main_layout)

    # noinspection PyArgumentList
    def add_widget(self, editor: QtWidgets.QWidget, field_name: str):
        if not field_name in self.information_model.title_name:
            return
        idx = self.information_model.title_name.index(field_name)
        self.main_layout.addRow(field_name, editor)
        self.mapper.addMapping(editor, idx)
        self.mapper.setItemDelegate(InformationDelegate())
        self.mapper.toFirst()

    def closeEvent(self, *args, **kwargs):
        if self.information_model.conn:
            self.information_model.conn.commit()
