#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from ...custom_widget import DateEdit, RealEdit, RateEdit, IntEdit, TextEdit, PercentEdit, LineEdit
from .detail_model import DetailModel


class DetailDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(DetailDelegate, self).__init__(parent)

    def createEditor(self, parent, option, model_index: QtCore.QModelIndex):
        model: DetailModel = model_index.model()
        if model.data_type[model_index.column()] == 'Date':
            editor = DateEdit(parent)
        elif model.data_type[model_index.column()] == 'Real':
            editor = RealEdit(parent)
        elif model.data_type[model_index.column()] == 'Rate':
            editor = RateEdit(parent)
        elif model.data_type[model_index.column()] == 'Int':
            editor = IntEdit(parent)
        elif model.data_type[model_index.column()] == 'Percent':
            editor = PercentEdit(parent)
        elif model.data_type[model_index.column()].split('(')[0] == 'Nchar':
            editor = TextEdit(parent, int(model.data_type[model_index.column()].split('(')[1].rstrip(')')))
        elif model.data_type[model_index.column()] == 'Bool':
            editor = QtCore.QVariant()
        else:
            editor = LineEdit(parent)
        return editor

    def setEditorData(self, editor, model_index: QtCore.QModelIndex):
        data = model_index.model().data(model_index, QtCore.Qt.EditRole)
        if isinstance(editor, LineEdit):
            if data:
                editor.setText(str(data))
            else:
                editor.setText('')
        else:
            editor.value = data

    def setModelData(self, editor, item_model: QtCore.QAbstractItemModel, model_index: QtCore.QModelIndex):
        if isinstance(editor, LineEdit):
            if editor.text():
                item_model.setData(model_index, editor.text())
            else:
                item_model.setData(model_index, None)
        else:
            item_model.setData(model_index, editor.value)
