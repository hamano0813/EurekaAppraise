#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp


class IntEdit(QLineEdit):
    def __init__(self, parent=None, *args):
        super(IntEdit, self).__init__(parent, *args)
        self.setAlignment(Qt.AlignRight)
        self.setValidator(QRegExpValidator(QRegExp('^[+-]?\\d*')))
        self.editingFinished.connect(self.get_int)

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
        self.setText(str(int(value)))
