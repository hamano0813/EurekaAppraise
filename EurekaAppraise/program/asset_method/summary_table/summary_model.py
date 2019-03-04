#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore

TYPE_DICT = {
    '_编号_': 'Nchar(10)',
    '_科目名称_': 'Nchar(60)',
    '_项目_': 'Nchar(60)',
    '_账面价值_': 'Real',
    '_账面原值_': 'Real',
    '_账面净值_': 'Real',
    '评估价值_': 'Real',
    '评估原值_': 'Real',
    '评估净值_': 'Real',
    '增减值_': 'Real',
    '原值增值额_': 'Real',
    '净值增值额_': 'Real',
    '增值率_': 'Percent',
    '原值增值率_': 'Percent',
    '净值增值率_': 'Percent',
}


class SummaryModel(QtCore.QAbstractTableModel):
    title_name: list
    data_type: list
    _data: list

    def __init__(self, conn: sqlite3.Connection, view_name: str, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.conn = conn
        self.view_name = view_name
        self.initialize_data(view_name)

    def initialize_data(self, view_name):
        c = self.conn.cursor()
        self._data = [list(row) for row in c.execute(f'SELECT * FROM [{view_name}];').fetchall()]
        self.title_name = [parameter[1] for parameter in c.execute(f'PRAGMA table_info([{view_name}]);').fetchall()]
        self.data_type = [TYPE_DICT[name] for name in self.title_name]
        c.close()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return [name.strip('_') for name in self.title_name][section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section + 1
        return QtCore.QVariant()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self.title_name)

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self._data)

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        value = self._data[index.row()][index.column()]
        data_type: str = self.data_type[index.column()]
        if role == QtCore.Qt.DisplayRole:
            if not value:
                return ''
            elif data_type == 'Percent':
                return f'{value * 100:,.02f}%'
            elif data_type == 'Real':
                return f'{value:,.02f}'
            elif data_type.startswith('Nchar'):
                return value
            return value
        elif role == QtCore.Qt.TextAlignmentRole:
            if value is None:
                return QtCore.QVariant()
            elif data_type in ('Percent', 'Real'):
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            return QtCore.QVariant()
        return QtCore.QVariant()

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QVariant()
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def copy_range(self, select_range):
        if select_range:
            r = max([index.row() for index in select_range]) - min([index.row() for index in select_range]) + 1
            c = max([index.column() for index in select_range]) - min([index.column() for index in select_range]) + 1
            return '\n'.join(['\t'.join([self.data(select_range[c * rid + cid], QtCore.Qt.DisplayRole)
                                         for cid in range(c)]) for rid in range(r)])
