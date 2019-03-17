#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from PyQt5 import QtCore, QtGui
from ...initialize_setting import EDIT_TABLE, SUMMARY_VIEW, SPECIAL_TABLE


class TreeItem:
    def __init__(self, row_item, parent=None):
        self.parent_item = parent
        self.row_item = row_item
        self.child_items = []

    def append_child(self, item):
        self.child_items.append(item)

    def child(self, row: int):
        return self.child_items[row]

    def child_count(self):
        return len(self.child_items)

    def column_count(self):
        return len(self.row_item)

    def data(self, column):
        try:
            return self.row_item[column]
        except IndexError:
            return None

    def parent(self):
        return self.parent_item

    def row(self):
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0


class AccountModel(QtCore.QAbstractItemModel):
    def __init__(self, conn: sqlite3.Connection, account_tree: dict, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.conn = conn
        self.root_item = TreeItem((self.tr('Code'), self.tr('Name')))
        self.add_data(account_tree, self.root_item)

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.root_item.column_count()

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid() or not self.conn:
            return QtCore.QVariant()
        if role == QtCore.Qt.TextColorRole:
            table = index.internalPointer().data(0)
            c = self.conn.cursor()
            try:
                if self.code(index) in EDIT_TABLE:
                    if c.execute(f'SELECT count(*) FROM [{table}];').fetchone()[0]:
                        return QtGui.QColor(QtCore.Qt.blue)
                elif self.code(index) in SUMMARY_VIEW:
                    if self.code(index, QtCore.Qt.DisplayRole) == '表1':
                        table = '表2'
                    if c.execute(f'''SELECT sum([小计]) FROM [{table}];''').fetchone()[0]:
                        return QtGui.QColor(QtCore.Qt.blue)
                elif self.code(index) in SPECIAL_TABLE:
                    if c.execute(f'''SELECT CASE WHEN sum([_账面价值_]) IS NULL THEN 0 ELSE sum([_账面价值_]) END +
                                            CASE WHEN sum([评估价值_]) IS NULL THEN 0 ELSE sum([评估价值_]) END
                                     FROM [{table}];''').fetchone()[0]:
                        return QtGui.QColor(QtCore.Qt.blue)
            except sqlite3.OperationalError as e:
                print(e)
            finally:
                c.close()
        if role != QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(index.column())

    @staticmethod
    def code(index: QtCore.QModelIndex, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not role == QtCore.Qt.DisplayRole:
            return None
        item = index.internalPointer()
        return item.data(0)

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section: int, orientation, role=None):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.root_item.data(section)
        return None

    def index(self, row: int, column: int, parent: TreeItem = None, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex = None):
        if not index.isValid():
            return QtCore.QModelIndex()
        child_item = index.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.root_item:
            return QtCore.QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
        return parent_item.child_count()

    def add_data(self, data, parent):
        for rid, ((code, name), setting) in enumerate(data.items()):
            parent.append_child(TreeItem([code, name], parent))
            if setting:
                self.add_data(setting, parent.child(rid))
