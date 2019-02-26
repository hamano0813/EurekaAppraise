#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore
from ..initialize_setting import *


class CreateDatabaseThread(QtCore.QObject):
    logPrinter = QtCore.pyqtSignal(str)
    errorPrinter = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()

    def __init__(self, conn: sqlite3.Connection, code: str, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.conn = conn
        self.code = code

    def work(self):
        self.create_table(BASIC_TABLE)
        self.create_table(ASSET_TABLE)
        self.finished.emit()

    def create_table(self, settings: dict):
        c = self.conn.cursor()
        for table_name, table_setting in settings.items():
            field_stmt = ',\n'.join(
                [f'\t[{field_name}] {data_type}' for field_name, data_type in table_setting.items()])
            try:
                c.execute(f'CREATE TABLE [{table_name}] (\n{field_stmt});')
                self.logPrinter.emit(self.tr('create table ') + f'{table_name}')
            except sqlite3.OperationalError as e:
                self.errorPrinter.emit(str(e))
        return c.close()

    def create_view(self, settings: dict):
        c = self.conn.cursor()
        for view_name, view_stmt in settings.items():
            try:
                c.execute(view_stmt)
                self.logPrinter.emit(self.tr('create view ') + f'{view_name}')
            except sqlite3.OperationalError as e:
                self.errorPrinter.emit(str(str(e)))
        return c.close()

    def insert_data(self, settings: dict):
        c = self.conn.cursor()
        for data_name, data_stmt in settings.items():
            try:
                c.execute(data_stmt)
            except sqlite3.OperationalError as e:
                self.errorPrinter.emit(str(e))
        return c.close()
