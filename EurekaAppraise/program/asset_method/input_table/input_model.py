#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore


class InputModel(QtCore.QAbstractTableModel):
    title_name: list
    row_title: list
    data_type: list
    col_formula: tuple
    row_formula: tuple
    _data: list

    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.range = self.operation = True
        self.conn = conn
        self.table_name = table_name
        self.initialize_data()

    def initialize_data(self):
        c = self.conn.cursor()
        parameters = c.execute(f'PRAGMA table_info([{self.table_name}]);').fetchall()
        self.title_name = [parameter[1] for parameter in parameters]
        self.data_type = [parameter[2].capitalize() for parameter in parameters]
        self.col_formula = c.execute(f"SELECT [强制], [等式] FROM [公式] WHERE [表名]='{self.table_name}';").fetchall()
        self.row_formula = c.execute(f"SELECT [强制], [等式] FROM [公式] WHERE [表名]='{self.table_name}r';").fetchall()
        self._data = [list(row) for row in c.execute(f'SELECT * FROM [{self.table_name}];').fetchall()]
        self.row_title = [row[0] for row in self._data]
        c.close()

    def headerData(self, section: int, orientation, role=QtCore.Qt.DisplayRole):
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
            return QtCore.QVariant()
        elif role == QtCore.Qt.TextAlignmentRole:
            if data_type in ('Percent', 'Real'):
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            return QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.EditRole:
            return value
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.EditRole:
            auto_columns = [formula.split('=')[0] for auto, formula in self.col_formula if auto]
            auto_rows = [formula.split('=')[0] for auto, formula in self.row_formula if auto]
            if self.title_name[index.column()] not in auto_columns or self.row_title[index.row()] not in auto_rows \
                    or self.operation:
                self._data[index.row()][index.column()] = value
            for formula_setting in self.col_formula:
                if self.title_name[index.column()] in formula_setting[1].split('=')[1]:
                    self.automatic_operation(index, formula_setting)
            for formula_setting in self.row_formula:
                if self.row_title[index.row()] in formula_setting[1].split('=')[1]:
                    self.automatic_row(index, formula_setting)
            if self.range:
                self.save_data()
            return True

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            QtCore.QVariant()
        if index.column() == 0:
            return QtCore.Qt.ItemIsEnabled
        for locking, formula in self.col_formula:
            if locking and self.title_name[index.column()] == formula.split('=')[0]:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        for locking, formula in self.row_formula:
            if locking and index.row() == self.row_title.index(formula.split('=')[0]):
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def automatic_row(self, index: QtCore.QModelIndex, formula_setting: tuple):
        auto, formula = formula_setting
        if auto or not self._data[self.row_title.index(formula.split('=')[0])][index.column()]:
            formula_text = formula.split('=')[1]
            for r_idx, title in enumerate(self.row_title):
                if self._data[r_idx][index.column()]:
                    formula_text = formula_text.replace(title, str(self._data[r_idx][index.column()]))
                else:
                    formula_text = formula_text.replace(title, '0')
            try:
                value = eval(formula_text)
            except (ZeroDivisionError, NameError, SyntaxError) as e:
                print(formula_text, e)
                value = None
            target_index = self.createIndex(self.row_title.index(formula.split('=')[0]), index.column())
            self.operation = True
            self.setData(target_index, value)
            self.operation = False

    def automatic_operation(self, index: QtCore.QModelIndex, formula_setting: tuple):
        auto, formula = formula_setting
        if auto or not self._data[index.row()][self.title_name.index(formula.split('=')[0])]:
            formula_text = formula.split('=')[1]
            for c_idx, title in enumerate(self.title_name):
                if self._data[index.row()][c_idx]:
                    formula_text = formula_text.replace(title, str(self._data[index.row()][c_idx]))
                else:
                    formula_text = formula_text.replace(title, '0')
            try:
                value = eval(formula_text)
            except (ZeroDivisionError, NameError) as e:
                value = None
            target_index = self.createIndex(index.row(), self.title_name.index(formula.split('=')[0]))
            self.operation = True
            self.setData(target_index, value)
            self.operation = False

    def paste_data(self, index: QtCore.QModelIndex, value):
        _value = None
        data_type: str = self.data_type[index.column()]
        if data_type == 'Percent':
            try:
                if '%' in str(value):
                    _value = float(str(value).replace(',', '', 5).replace('%', '')) / 100
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type == 'Real':
            try:
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type.startswith('Nchar'):
            try:
                _value = str(value).strip()[0: int(data_type.split('(')[1].rstrip(')'))]
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        self.setData(index, _value)

    def copy_range(self, select_range):
        if select_range:
            r = max([index.row() for index in select_range]) - min([index.row() for index in select_range]) + 1
            r -= 1 if max([index.row() for index in select_range]) == self.rowCount() - 1 else 0
            c = max([index.column() for index in select_range]) - min([index.column() for index in select_range]) + 1
            return '\n'.join(['\t'.join([self.data(select_range[c * rid + cid], QtCore.Qt.DisplayRole)
                                         for cid in range(c)]) for rid in range(r)])

    def paste_range(self, select_range: list, text_data: str):
        if select_range and text_data:
            start_row = min([index.row() for index in select_range])
            start_column = min([index.column() for index in select_range])
            temp_data = [row.split('\t') for row in text_data.split('\n') if row is not None]
            add_rows = len(temp_data) + start_row + 1 - self.rowCount()
            if add_rows > 0:
                self.insertRows(self.rowCount() - 1, add_rows)
            max_column = self.columnCount() - start_column
            if max_column < max(map(len, temp_data)):
                data = [row_data[0: max_column] for row_data in temp_data]
            else:
                data = temp_data
            self.range = False
            for rid, row_data in enumerate(data):
                for cid, value in enumerate(row_data):
                    idx = self.createIndex(start_row + rid, start_column + cid)
                    self.paste_data(idx, value)
            self.save_data()
            self.range = True

    def delete_range(self, select_range: list):
        self.range = False
        [self.setData(index, None) for index in select_range[::-1] if index.row() < self.rowCount() - 1]
        self.save_data()
        self.range = True

    def save_data(self):
        c = self.conn.cursor()
        c.execute(f'DELETE FROM [{self.table_name}];')
        placeholder = ', '.join((['?'] * self.columnCount()))
        c.executemany(f'INSERT INTO [{self.table_name}] VALUES ({placeholder})', self._data)
        c.close()
        self.conn.commit()
