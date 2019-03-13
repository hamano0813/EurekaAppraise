#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets


class BoolCheck(QtWidgets.QCheckBox):
    def __init__(self, parent=None, *args):
        QtWidgets.QCheckBox.__init__(self, parent, *args)

    @property
    def value(self):
        return self.isChecked()

    @value.setter
    def value(self, check: bool):
        self.setChecked(check)
