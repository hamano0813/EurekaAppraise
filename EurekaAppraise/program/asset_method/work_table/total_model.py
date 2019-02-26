#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class TotalModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(TotalModel, self).__init__(parent)
        self._summary = [None]

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return 1

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self._summary)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return '合计'
        return QtCore.QVariant()

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.DisplayRole:
            if self._summary[index.column()]:
                # noinspection PyTypeChecker
                return f'{float(self._summary[index.column()]):,.02f}'
            else:
                return ''
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        return QtCore.QVariant()

    def set_total(self, data):
        self.beginResetModel()
        self._summary = data
        self.endResetModel()

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QVariant()
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def copy_range(self, select_range):
        if select_range:
            c = max([index.column() for index in select_range]) - min([index.column() for index in select_range]) + 1
            return '\t'.join([self.data(select_range[cid], QtCore.Qt.DisplayRole) for cid in range(c)])
