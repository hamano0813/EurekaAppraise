#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore
from ..initialize_setting import *


class CreateProjectThread(QtCore.QThread):
    conn: sqlite3.Connection
    logPrinter = QtCore.pyqtSignal(str)
    errorPrinter = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, file: str, code: str, parent=None):
        QtCore.QObject.__init__(self, parent)
        self.file = file
        self.code = code

    def run(self):
        self.conn = sqlite3.connect(self.file)
        self.create_table(BASIC_TABLE)
        self.create_table(ASSET_TABLE)
        self.create_table(SPECIAL_TABLE)

        self.insert_data(ASSET_INSERT)
        self.conn.close()
        self.conn = None
        self.logPrinter.emit(self.tr('create project completed'))
        self.finished.emit(self.file)

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
                self.errorPrinter.emit(str(e))
        return c.close()

    def insert_data(self, settings: dict):
        c = self.conn.cursor()
        for table_name, field_settings in settings.items():
            field, data =  field_settings
            try:
                c.executemany(f'INSERT INTO [{table_name}] ({field}) VALUES (?)', data)
                self.conn.commit()
                self.logPrinter.emit(self.tr('insert data to ' + f'{table_name}'))
            except sqlite3.OperationalError as e:
                self.errorPrinter.emit(str(e))
        return c.close()
