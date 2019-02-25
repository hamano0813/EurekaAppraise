#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import datetime
from PyQt5 import QtWidgets, QtCore


class CreateSpin(QtWidgets.QSpinBox):
    def __init__(self, min_value: int, max_value: int, default: int = None, parent=None):
        super(CreateSpin, self).__init__(parent)
        self.setRange(min_value, max_value)
        self.setValue(default) if default else self.setValue(min_value)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setFixedWidth(80)

    def valueFromText(self, text: str) -> int:
        if text:
            return int(text)
        return self.minimum()

    def textFromValue(self, val: int) -> str:
        return f'{val:0{len(str(self.minimum()))}d}'


class CreateDialog(QtWidgets.QDialog):
    # noinspection PyArgumentList
    def __init__(self, parent=None,
                 flags=QtCore.Qt.CustomizeWindowHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool):
        super(CreateDialog, self).__init__(parent, flags)
        self.year_spin = CreateSpin(2015, 2030, datetime.date.today().year)
        self.code_spin = CreateSpin(100, 999)

        accept_button = QtWidgets.QPushButton(self.tr('Confirm'))
        reject_button = QtWidgets.QPushButton(self.tr('Cancel'))
        button_box = QtWidgets.QDialogButtonBox()
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.addButton(accept_button, QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(reject_button, QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(QtWidgets.QLabel(self.tr('Project Year')), 0, 0, 1, 1)
        main_layout.addWidget(QtWidgets.QLabel(self.tr('Project Code')), 1, 0, 1, 1)
        main_layout.addWidget(self.year_spin, 0, 1, 1, 1)
        main_layout.addWidget(self.code_spin, 1, 1, 1, 1)
        main_layout.addWidget(button_box, 2, 0, 1, 2, QtCore.Qt.AlignRight)

        self.setLayout(main_layout)

    def get_project_path(self) -> (str, str):
        config = configparser.ConfigParser()
        config.read('config.ini')
        path = config.get('path', 'default_folder')
        if self.exec_():
            project_code = self.year_spin.text() + '-' + self.code_spin.text()
            return path + '/' + project_code + '.db3', project_code
        return None, None
