#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from .summary_model import SummaryModel

CHARACTER_WIDTH = 15
ROW_HEIGHT = 25


class SummaryView(QTableView):
    def __init__(self, parent=None):
        QTableView.__init__(self, parent)
        self.setModel = self.set_width(self.setModel)
        self.setSelectionBehavior(QTableView.SelectRows | QTableView.SelectColumns)
        self.verticalHeader().setFixedWidth(50)
        self.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.verticalHeader().setSectionsClickable(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setWordWrap(False)
        self.keyPressEvent = self.key_press(self.keyPressEvent)

    def set_width(self, func):
        def wrapper(model: SummaryModel):
            func(model)
            for idx, data_type in enumerate(model.data_type):
                title_width = len(model.title_name[idx]) * CHARACTER_WIDTH
                if data_type == 'Real':
                    self.setColumnWidth(idx, max(120, title_width))
                elif data_type == 'Percent':
                    self.setColumnWidth(idx, max(70, title_width))
                elif data_type.startswith('Nchar'):
                    self.setColumnWidth(idx, max(int(data_type.split('(')[1].rstrip(')')) * 5, title_width))
            self.reset_height()
            model.rowsInserted.connect(self.reset_height)

        return wrapper

    def reset_height(self):
        for idx in range(self.model().rowCount()):
            self.setRowHeight(idx, ROW_HEIGHT)

    def key_press(self, func):
        # noinspection PyArgumentList
        def wrapper(event: QKeyEvent):
            if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
                QApplication.clipboard().setText(self.model().copy_range(self.selectedIndexes()))
            else:
                func(event)

        return wrapper
