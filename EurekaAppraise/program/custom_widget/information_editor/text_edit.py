#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


class TextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self, length=20, parent=None):
        QtWidgets.QPlainTextEdit.__init__(self, parent)
        self.setFixedSize(300, (length // 24 + 1) * 22)
        self.setMaximumBlockCount((length // 24 + 1))

    @property
    def value(self):
        return self.toPlainText()

    @value.setter
    def value(self, text):
        if text:
            self.setPlainText(text)
