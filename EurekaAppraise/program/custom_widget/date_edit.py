#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDateEdit, QCalendarWidget
from PyQt5.QtCore import QDate


class DateEdit(QDateEdit):
    def __init__(self, parent=None, *args):
        super(DateEdit, self).__init__(parent, *args)
        self.setCalendarPopup(True)
        self.setDisplayFormat('yyyy-MM-dd')
        self.calendarWidget().setGridVisible(True)
        self.calendarWidget().setHorizontalHeaderFormat(QCalendarWidget.NoHorizontalHeader)
        self.calendarWidget().setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

    @property
    def value(self):
        if self.date().toString('yyyy-MM-dd') == '2000-01-01':
            return None
        return self.date().toString('yyyy-MM-dd')

    @value.setter
    def value(self, value):
        if not value:
            self.setDate(QDate(2000, 1, 1))
        else:
            self.setDate(QDate().fromString(value, 'yyyy-MM-dd'))
