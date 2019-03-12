#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore


class InformationModel(QtCore.QAbstractTableModel):
    title_name: list
    _data: list

    def __init__(self, conn: sqlite3.Connection, table_name: str, parent):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.conn = conn
        self.table_name = table_name
        self.initialize_data()

    def initialize_data(self):
        c = self.conn.cursor()
        parameters = c.execute(f'PRAGMA table_info([{self.table_name}]);').fetchall()
        self.title_name = [parameter[1] for parameter in parameters]
        self._data = [list(row) for row in c.execute(f'SELECT * FROM [{self.table_name}];').fetchall()][0]
        c.close()

    def rowCount(self, parent=None, *args, **kwargs):
        return 1

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._data)

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole:
            c = self.conn.cursor()
            sql = f'SELECT [{self.title_name[index.column()]}] FROM [{self.table_name}];'
            c.execute(sql)
            value = c.fetchone()[0]
            c.close()
            return value
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole and self.conn:
            if value is None:
                value = ''
            c = self.conn.cursor()
            sql = f"UPDATE [{self.table_name}] SET [{self.title_name[index.column()]}]='{value}';"
            c.execute(sql)
            c.close()
            self.conn.commit()
