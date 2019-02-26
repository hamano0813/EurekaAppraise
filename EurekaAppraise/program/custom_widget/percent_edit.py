#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp


class PercentEdit(QLineEdit):
    def __init__(self, parent=None, *args):
        super(PercentEdit, self).__init__(parent, *args)
        self.setAlignment(Qt.AlignRight)
        self.setValidator(QRegExpValidator(QRegExp('^[+-]?\\d*(\\.\\d{0,2})?')))
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
