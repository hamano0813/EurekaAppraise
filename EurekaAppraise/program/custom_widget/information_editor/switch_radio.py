#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore


class SwitchRadio(QtWidgets.QFrame):
    def __init__(self, switch_items: list, parent=None, flags=QtCore.Qt.FramelessWindowHint):
        QtWidgets.QFrame.__init__(self, parent, flags)
        self.switch_items = switch_items
        self.checkbox_list = []
        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        for idx, item in enumerate(self.switch_items):
            checkbox = QtWidgets.QCheckBox(item)
            self.button_group.addButton(checkbox, idx)
            main_layout.addWidget(checkbox, alignment=QtCore.Qt.AlignVCenter)

        self.setLayout(main_layout)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

    @property
    def value(self):
        for checkbox in self.button_group.buttons():
            if checkbox.isChecked():
                return checkbox.text()

    @value.setter
    def value(self, value_text: str):
        if value_text in self.switch_items:
            self.button_group.button(self.switch_items.index(value_text)).setChecked(True)
