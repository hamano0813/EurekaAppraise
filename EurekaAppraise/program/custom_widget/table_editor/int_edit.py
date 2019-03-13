#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui


class IntEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, *args):
        QtWidgets.QLineEdit.__init__(self, parent, *args)
        self.setMinimumHeight(22)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[+-]?\\d*')))
        self.editingFinished.connect(self.get_int)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)

    def get_int(self):
        if self.displayText():
            self.setText(str(int(self.text())))
        else:
            self.setText('')

    @property
    def value(self):
        if self.displayText().strip() == '':
            return None
        return int(self.text())

    @value.setter
    def value(self, value):
        if not value:
            self.setText('')
        else:
            self.setText(str(int(value)))
