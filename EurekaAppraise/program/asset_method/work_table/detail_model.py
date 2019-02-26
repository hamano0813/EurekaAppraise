#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from dateutil import parser
from PyQt5 import QtCore


class DetailModel(QtCore.QAbstractTableModel):
    totalChanged = QtCore.pyqtSignal(list)
    detailChanged = QtCore.pyqtSignal(bool)

    def __init__(self, conn: sqlite3.Connection, table_name: str, parent=None):
        super(DetailModel, self).__init__(parent)
        self.allows = True
        self.conn = conn
        self.table_name = table_name
        self._data, self.title_name, self.data_type, self.auto_formula, self.basic_date = self.set_table(table_name)

    def set_table(self, table_name):
        c = self.conn.cursor()
        parameters = c.execute(f'PRAGMA table_info([表{table_name}]);').fetchall()
        title_name = [parameter[1] for parameter in parameters]
        data_type = [parameter[2].capitalize() for parameter in parameters]
        auto_formula = c.execute(f"SELECT [强制], [等式] FROM [公式] WHERE [表名]='表{table_name}';").fetchall()
        basic_date = parser.parser(c.execute(f'SELECT [评估基准日] FROM [基础信息];').fetchall()[0][0])
        raw_data = [list(row) for row in c.execute(f'SELECT * FROM [表{table_name}];').fetchall()]
        c.close()
        return raw_data, title_name, data_type, auto_formula, basic_date

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
        elif role == QtCore.Qt.DisplayRole:
            if index.row() == self.rowCount() - 1 or self._data[index.row()][index.column()] is None:
                return ''
            elif self.data_type[index.column()] == 'Date':
                try:
                    return parser.parser(self._data[index.row()][index.column()]).strftime('%Y-%m-%d')
                except ValueError as e:
                    print(e)
                    return self._data[index.row()][index.column()]
            elif self.data_type[index.column()] == 'Percent':
                return f'{self._data[index.row()][index.column()] * 100:,.02f}%'
            elif self.data_type[index.column()] == 'Int':
                # noinspection PyTypeChecker
                return f'{int(self._data[index.row()][index.column()]):,d}'
            elif self.data_type[index.column()] == 'Real':
                return f'{self._data[index.row()][index.column()]:,.02f}'
            elif self.data_type[index.column()] == 'Rate':
                return f'{self._data[index.row()][index.column()]:,.04f}'
            elif self.data_type[index.column()].split('(')[0] == 'Nchar':
                return self._data[index.row()][index.column()]
            return QtCore.QVariant()
        elif role == QtCore.Qt.TextAlignmentRole:
            if index.row() == self.rowCount() - 1 or self._data[index.row()][index.column()] is None:
                return QtCore.QVariant()
            elif self.data_type[index.column()] in ('Percent', 'Int', 'Real', 'Rate'):
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
            elif self.data_type[index.column()] == 'Bool':
                return QtCore.Qt.AlignCenter
            return QtCore.QVariant()
        elif role == QtCore.Qt.CheckStateRole:
            return QtCore.Qt.Checked if self._data[index.row()][index.column()] else QtCore.Qt.Unchecked
        elif role == QtCore.Qt.EditRole:
            if index.row() == self.rowCount() - 1 or self._data[index.row()][index.column()] is None:
                return None
            return self._data[index.row()][index.column()]
        return QtCore.QVariant()

    # noinspection PyTypeChecker
    def setData(self, index: QtCore.QModelIndex, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return QtCore.QVariant()

        if role == QtCore.Qt.CheckStateRole and self.data_type[index.column()] == 'Bool':
            if value == QtCore.Qt.Checked:
                self._data[index.row()][index.column()] = True
            else:
                self._data[index.row()][index.column()] = False
        elif role == QtCore.Qt.EditRole:
            if index.row() == self.rowCount() - 1:
                self.insertRows(index.row())
            self._data[index.row()][index.column()] = value
            for formula_setting in self.auto_formula:
                if self.title_name[index.column()] in formula_setting[1].split('=')[1]:
                    self.automatic_operation(index, formula_setting)
            for row in range(self.rowCount() - 2, -1, -1):
                if any(self._data[row]):
                    break
                self.removeRows(row)
            self.totalChanged.emit(self.total)
            self.detailChanged.emit(False)
            if self.allows:
                self.save_data()
            return True

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid() or index.row() == self.rowCount() - 1:
            return QtCore.QVariant()
        for locking, formula in self.auto_formula:
            if locking and self.title_name[index.column()] == formula.split('=')[0]:
                return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        if self.data_type[index.column()] == 'Bool':
            return QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex(), *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self._data.insert(position + row, [None] * self.columnCount())
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex(), *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), position, position + rows - 1)
        self._data = self._data[:position] + self._data[position + rows:]
        self.endRemoveRows()
        return True

    @property
    def total(self):
        return [sum([self._data[i][c_idx] if self._data[i][c_idx] else 0 for i in range(self.rowCount() - 1)])
                if self.data_type[c_idx] == 'Real' else None for c_idx in range(self.columnCount())]

    def automatic_operation(self, index: QtCore.QModelIndex, formula_setting: tuple):
        auto, formula = formula_setting
        if auto or not self._data[index.row()][self.title_name.index(formula.split('=')[0])]:
            formula_text = formula.split('=')[1]
            for c_idx, title in enumerate(self.title_name):
                if self._data[index.row()][c_idx]:
                    formula_text = formula_text.replace(title, str(self._data[index.row()][c_idx]))
            try:
                value = eval(formula_text)
            except NameError as e:
                print(e)
                value = None
            self._data[index.row()][self.title_name.index(formula.split('=')[0])] = value

    def aging(self, date_text):
        try:
            date = parser.parser(date_text)
        except ValueError as e:
            print(e)
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

    def paste_range(self, select_range: list, text_data: str):
        if select_range and text_data:
            start_row = min([index.row() for index in select_range])
            start_column = min([index.column() for index in select_range])
            temp_data = [row.split('\t') for row in text_data.split('\n') if row]
            add_rows = len(temp_data) + start_row + 1 - self.rowCount()
            if add_rows > 0:
                self.insertRows(self.rowCount() - 1, add_rows)
            max_column = self.columnCount() - start_column
            if max_column < max(map(len, temp_data)):
                data = [row_data[0: max_column] for row_data in temp_data]
            else:
                data = temp_data
            self.allows = False
            for rid, row_data in enumerate(data):
                for cid, value in enumerate(row_data):
                    idx = self.createIndex(start_row + rid, start_column + cid)
                    self.paste_data(idx, value)
            self.save_data()
            self.allows = True
            return True

    def paste_data(self, index: QtCore.QModelIndex, value):
        _value = None
        if self.data_type[index.column()] == 'Date':
            try:
                _value = str(parser.parser(value)) if str(parser.parser(value)) != 'NaT' else None
            except ValueError as e:
                print(e)
        elif self.data_type[index.column()] == 'Percent':
            try:
                if '%' in str(value):
                    _value = float(str(value).replace(',', '', 5).replace('%', '')) / 100
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(e)
        elif self.data_type[index.column()] == 'Int':
            try:
                _value = int(str(value).replace(',', '', 5))
            except ValueError as e:
                print(e)

        elif self.data_type[index.column()] in ('Real', 'Rate'):
            try:
                _value = float(str(value).replace(',', '', 5))
            except ValueError as e:
                print(e)
        elif self.data_type[index.column()].split('(')[0] == 'Nchar':
            try:
                _value = str(value)
            except ValueError as e:
                print(e)

        self.setData(index, _value)

    def copy_range(self, select_range):
        if select_range:
            r = max([index.row() for index in select_range]) - min([index.row() for index in select_range]) + 1
            r -= 1 if max([index.row() for index in select_range]) == self.rowCount() - 1 else 0
            c = max([index.column() for index in select_range]) - min([index.column() for index in select_range]) + 1
            return '\n'.join(
                ['\t'.join([self.data(select_range[c * rid + cid], QtCore.Qt.DisplayRole) for cid in range(c)])
                 for rid in range(r)])

    def save_data(self):
        c = self.conn.cursor()
        c.execute(f'DELETE FROM [表{self.table_name}];')
        placeholder = ', '.join((['?'] * self.columnCount()))
        c.executemany(f'INSERT INTO [表{self.table_name}] VALUES ({placeholder})', self._data)
        c.close()
        self.conn.commit()
