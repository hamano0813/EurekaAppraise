#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore


class DateEdit(QtWidgets.QDateEdit):
    def __init__(self, parent=None, *args):
        QtWidgets.QDateEdit.__init__(self, parent, *args)
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy-MM-dd')
        self.calendarWidget().setGridVisible(True)
        self.calendarWidget().setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)

    @property
    def value(self):
        if self.date().toString('yyyy-MM-dd') == '2000-01-01':
            return None
        return self.date().toString('yyyy-MM-dd')

    @value.setter
    def value(self, value):
        print(value)
        if not value:
            self.setDate(QtCore.QDate(2000, 1, 1))
        else:
            self.setDate(QtCore.QDate().fromString(value, 'yyyy-MM-dd'))
