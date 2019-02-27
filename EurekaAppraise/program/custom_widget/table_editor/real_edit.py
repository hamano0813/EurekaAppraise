#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui


class RealEdit(QtWidgets.QLineEdit):
    def __init__(self, parent=None, *args):
        QtWidgets.QLineEdit.__init__(self, parent, *args)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('^[+-]?\\d*(\\.\\d{0,2})?')))
        self.editingFinished.connect(self.get_real)

    def get_real(self):
        if self.displayText():
            self.setText(f'{float(self.text()):.2f}')
        else:
            self.setText('')

    @property
    def value(self):
        if self.displayText().strip() == '':
            return None
        return float(self.text())

    @value.setter
    def value(self, value):
        if value is None:
            self.setText('')
        else:
            self.setText(f'{float(value):.2f}')
