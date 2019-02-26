#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp


class RateEdit(QLineEdit):
    def __init__(self, parent=None, *args):
        super(RateEdit, self).__init__(parent, *args)
        self.setAlignment(Qt.AlignRight)
        self.setValidator(QRegExpValidator(QRegExp('^[+-]?\\d*(\\.\\d{0,4})?')))
        self.editingFinished.connect(self.get_real)

    def get_real(self):
        if self.displayText():
            self.setText(f'{float(self.text()):.4f}')
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
            self.setText(f'{float(value):.4f}')
