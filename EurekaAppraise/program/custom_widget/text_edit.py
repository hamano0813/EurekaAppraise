#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLineEdit


class TextEdit(QLineEdit):
    def __init__(self, parent, length=20, *args):
        super(TextEdit, self).__init__(parent, *args)
        self.setMaxLength(length)

    @property
    def value(self):
        if self.displayText().strip() == '':
            return None
        return self.text().strip()[0: self.maxLength()]

    @value.setter
    def value(self, text):
        if text:
            self.setText(str(text))
        else:
            self.setText('')
