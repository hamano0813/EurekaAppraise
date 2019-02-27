#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui


class PercentEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, *args):
        QtWidgets.QLineEdit.__init__(self, parent, *args)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[+-]?\\d*(\\.\\d{0,2})?')))
        self.editingFinished.connect(self.get_percent)

    def get_percent(self):
        if self.displayText():
            self.setText(f'{float(self.text()):.2f}')
        else:
            self.setText('')

    @property
    def value(self):
        if self.displayText().strip() == '':
            return None
        return float(self.text()) / 100

    @value.setter
    def value(self, value):
        if not value:
            self.setText('')
        else:
            self.setText(f'{value * 100:.2f}')
