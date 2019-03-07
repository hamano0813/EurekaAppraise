#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from ...custom_widget.table_editor import *
from .input_model import InputModel

EDITOR = {
    'Real': RealEdit,
    'Percent': PercentEdit
}


class InputDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        model: InputModel = index.model()
        data_type: str = model.data_type[index.column()]
        if data_type.startswith('Nchar'):
            editor = LineEdit(parent, int(data_type.split('(')[1].rstrip(')')))
        elif data_type in EDITOR:
            editor = EDITOR[data_type](parent)
        else:
            editor = QtWidgets.QLineEdit(parent)
        return editor

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
            if editor.text():
                item_model.setData(index, editor.text())
            else:
                item_model.setData(index, None)
        else:
            item_model.setData(index, editor.value)
