#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore


class InformationDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def setEditorData(self, editor, index: QtCore.QModelIndex):
        data = index.model().data(index, QtCore.Qt.EditRole)
        if type(QtWidgets.QLineEdit) == editor:
            if data:
                editor.setText(str(data))
            else:
                editor.setText('')
        else:
            editor.value = data

    def setModelData(self, editor, item_model: QtCore.QAbstractItemModel, index: QtCore.QModelIndex):
        if type(QtWidgets.QLineEdit) == editor:
            if editor.text() is not None:
                item_model.setData(index, editor.text())
            else:
                item_model.setData(index, None)
        else:
            item_model.setData(index, editor.value)
