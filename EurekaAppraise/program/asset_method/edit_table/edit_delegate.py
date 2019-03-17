#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore, QtGui
from ...custom_widget.table_editor import *
from .edit_model import EditModel

EDITOR = {
    'Date': DateEdit,
    'Real': RealEdit,
    'Rate': RateEdit,
    'Int': IntEdit,
    'Percent': PercentEdit
}


class EditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        model: EditModel = index.model()
        dtype: str = model.dtype[index.column()]
        if dtype == 'Bool':
            checkbox_option = QtWidgets.QStyleOptionButton()
            checkbox_option.rect = option.rect
            checkbox_option.rect.moveLeft(option.rect.x() + option.rect.width() // 2 - 6)
            checkbox_option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_Active
            if model.data(index, role=QtCore.Qt.EditRole):
                checkbox_option.state |= QtWidgets.QStyle.State_On
            else:
                checkbox_option.state |= QtWidgets.QStyle.State_Off
            # noinspection PyArgumentList
            return QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_CheckBox, checkbox_option, painter)
        return QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)

    def editorEvent(self, event: QtCore.QEvent, model: QtCore.QAbstractItemModel, option, index: QtCore.QModelIndex):
        model: EditModel = index.model()
        dtype: str = model.dtype[index.column()]
        rect: QtCore.QRect = option.rect
        if event.type() == QtCore.QEvent.MouseButtonPress and rect.contains(event.pos()):
            if dtype == 'Bool':
                value = model.data(index, QtCore.Qt.EditRole)
                value = False if value else True
                return model.setData(index, value, QtCore.Qt.EditRole)
        return QtWidgets.QStyledItemDelegate.editorEvent(self, event, model, option, index)

    def createEditor(self, parent, option, index: QtCore.QModelIndex):
        model: EditModel = index.model()
        dtype: str = model.dtype[index.column()]
        if dtype.startswith('Nchar'):
            editor = LineEdit(int(dtype.split('(')[1].rstrip(')')), parent)
        elif dtype == 'Bool':
            editor = QtCore.QVariant()
        elif dtype in EDITOR:
            editor = EDITOR[dtype](parent)
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

    def updateEditorGeometry(self, editor, option, index: QtCore.QModelIndex):
        editor.setGeometry(option.rect)
