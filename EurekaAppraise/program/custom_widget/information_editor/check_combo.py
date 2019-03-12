#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets


class CheckCombo(QtWidgets.QComboBox):
    def __init__(self, check_items: list, parent=None):
        QtWidgets.QComboBox.__init__(self, parent)
        self.check_items = check_items
        self.checkbox_list = []
        self.setLineEdit(QtWidgets.QLineEdit())
        self.lineEdit().setReadOnly(True)
        self.list_widget = QtWidgets.QListWidget()

        for idx, item in enumerate(self.check_items):
            checkbox = QtWidgets.QCheckBox(item)
            checkbox.stateChanged.connect(self.refresh)
            check = QtWidgets.QListWidgetItem(self.list_widget)
            self.list_widget.setItemWidget(check, checkbox)
            self.checkbox_list.append(checkbox)
        self.setModel(self.list_widget.model())
        self.setView(self.list_widget)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

    def refresh(self):
        self.lineEdit().setReadOnly(False)
        self.lineEdit().clear()
        text = '、'.join([checkbox.text() for checkbox in self.checkbox_list if checkbox.isChecked()])
        self.lineEdit().setText(text)
        self.lineEdit().setReadOnly(True)

    @property
    def value(self):
        return self.lineEdit().text()

    @value.setter
    def value(self, value_text: str):
        if value_text:
            for item in value_text.split('、'):
                self.lineEdit().setReadOnly(False)
                if item in self.check_items:
                    check_idx = self.check_items.index(item)
                    self.checkbox_list[check_idx].setChecked(True)
                else:
                    checkbox = QtWidgets.QCheckBox(item)
                    checkbox.stateChanged.connect(self.refresh)
                    check = QtWidgets.QListWidgetItem(self.list_widget)
                    self.list_widget.setItemWidget(check, checkbox)
                    self.checkbox_list.append(checkbox)
                    checkbox.setChecked(True)
                self.lineEdit().setReadOnly(True)
