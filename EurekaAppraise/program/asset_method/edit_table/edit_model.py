#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import datetime
from dateutil import parser
from PyQt5 import QtCore


class EditModel(QtCore.QAbstractTableModel):
    totalChanged = QtCore.pyqtSignal(list)
    title_name: list
    data_type: list
    auto_formula: tuple
    basic_date: datetime.datetime
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
        self.auto_formula = c.execute(f"SELECT [强制], [等式] FROM [公式] WHERE [表名]='{self.table_name}';").fetchall()
        self.basic_date = parser.parse(c.execute(f'SELECT [评估基准日] FROM [基础信息];').fetchall()[0][0])
        self._data = [list(row) for row in c.execute(f'SELECT * FROM [{self.table_name}];').fetchall()]
        c.close()

    def headerData(self, section: int, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return [name.strip('_') for name in self.title_name][section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            if section == self.rowCount() - 1:
                return '*'
            return section + 1
        return QtCore.QVariant()

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self.title_name)

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self._data) + 1

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        last_row = index.row() == self.rowCount() - 1
        value = None if last_row else self._data[index.row()][index.column()]
        data_type: str = self.data_type[index.column()]
        if role == QtCore.Qt.DisplayRole:
            if last_row or value is None:
                return ''
            elif data_type == 'Date':
                try:
                    return parser.parse(value).strftime('%Y-%m-%d')
                except ValueError as e:
                    print(value, e)
                    return value
            elif data_type == 'Percent':
                return f'{value * 100:,.02f}%'
            elif data_type == 'Int':
                return f'{value:,d}'
            elif data_type == 'Real':
                return f'{value:,.02f}'
            elif data_type == 'Rate':
                return f'{value:,.04f}'
            elif data_type == 'Bool':
                return '√' if value else ''
            elif data_type.startswith('Nchar'):
                return value
            return QtCore.QVariant()
        elif role == QtCore.Qt.TextAlignmentRole:
            if data_type in ('Percent', 'Int', 'Real', 'Rate'):
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            return QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.EditRole:
            return value
        return QtCore.QVariant()

    def setData(self, index: QtCore.QModelIndex, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return QtCore.QVariant()
        last_row = index.row() == self.rowCount() - 1
        auto_columns = [formula.split('=')[0] for auto, formula in self.auto_formula if auto]
        if last_row:
            self.insertRows(index.row())
        if role == QtCore.Qt.EditRole:
            if self.title_name[index.column()] not in auto_columns or self.operation:
                self._data[index.row()][index.column()] = value
            for formula_setting in self.auto_formula:
                if self.title_name[index.column()] in formula_setting[1].split('=')[1]:
                    self.automatic_operation(index, formula_setting)
            for row in range(self.rowCount() - 2, -1, -1):
                if any(self._data[row]):
                    break
                self.removeRows(row)
            if self.range:
                self.save_data()

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            QtCore.QVariant()
        for locking, formula in self.auto_formula:
            if locking and self.title_name[index.column()] == formula.split('=')[0]:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def sort(self, column_id, order=None):
        def get_sorted_key(row_data):
            if row_data[column_id]:
                return row_data[column_id]
            elif self.data_type[column_id].startswith('Nchar') or self.data_type[column_id] == 'Date':
                return ''
            return 0

        self.layoutAboutToBeChanged.emit()
        self._data = sorted(self._data, key=get_sorted_key, reverse=order == QtCore.Qt.AscendingOrder)
        self.save_data()
        self.layoutChanged.emit()

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self._data.insert(position + row, [None] * self.columnCount())
        self.endInsertRows()

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
        self._data = self._data[:position] + self._data[position + rows:]
        self.endRemoveRows()

    @property
    def total(self):
        return [sum([self._data[i][c_idx] if self._data[i][c_idx] else 0 for i in range(self.rowCount() - 1)])
                if self.data_type[c_idx] in ('Real', 'Int') else None for c_idx in range(self.columnCount())]

    def automatic_operation(self, index: QtCore.QModelIndex, formula_setting: tuple):
        auto, formula = formula_setting
        if auto or not self._data[index.row()][self.title_name.index(formula.split('=')[0])]:
            formula_text = formula.split('=')[1]
            for c_idx, title in enumerate(self.title_name):
                if not index.row() == self.rowCount() - 1 and self._data[index.row()][c_idx]:
                    formula_text = formula_text.replace(title, str(self._data[index.row()][c_idx]))
                else:
                    formula_text: str = formula_text.replace(title, '0')
                if formula_text.endswith('/0'):
                    formula_text = 'None'
            try:
                value = eval(formula_text)
            except (ZeroDivisionError, NameError) as e:
                print(formula_text, e)
                value = None
            target_index = self.createIndex(index.row(), self.title_name.index(formula.split('=')[0]))
            self.operation = True
            self.setData(target_index, value)
            self.operation = False

    def aging(self, date_text):
        try:
            date = parser.parse(date_text)
        except ValueError as e:
            print(date_text, e)
            return None
        months = (self.basic_date.year - date.year) * 12 + (self.basic_date.month - date.month)
        if not months:
            return None
        elif months < 0:
            return '超出基准日'
        elif not months // 12:
            return f'{months % 12}月'
        elif not months % 12:
            return f'{months // 12}年'
        else:
            return f'{months // 12}年{months % 12}月'

    def paste_data(self, index: QtCore.QModelIndex, value):
        _value = None
        data_type: str = self.data_type[index.column()]
        if data_type == 'Date':
            try:
                d_str = value.replace('年', '-').replace('月', '-').replace('日', '-')
                d_str = d_str + '1' if d_str.endswith('-') else d_str
                _value = str(parser.parse(d_str).strftime('%Y-%m-%d')) if str(parser.parse(d_str)) != 'NaT' else None
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type == 'Percent':
            try:
                if '%' in str(value):
                    _value = float(str(value).replace(',', '', 5).replace('%', '')) / 100
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type == 'Int':
            try:
                _value = int(float(str(value).replace(',', '', 5)))
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type in ('Real', 'Rate'):
            try:
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(value, index.row(), index.column(), e)
        elif data_type == 'Bool':
            try:
                _value = True if str(value).strip() == '√' else False
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
                    idx: QtCore.QModelIndex = self.createIndex(start_row + rid, start_column + cid)
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
        self.totalChanged.emit(self.total)
