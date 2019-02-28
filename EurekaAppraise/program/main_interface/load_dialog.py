#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
import configparser
from PyQt5 import QtWidgets, QtCore


class ProjectTableModel(QtCore.QAbstractTableModel):
    def __init__(self, project_table: list, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.project_table = project_table
        self.title_list = [self.tr('Code'), self.tr('Project Name')]

    def headerData(self, section: int, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.title_list[section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return section + 1
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return len(self.project_table)

    def columnCount(self, parent=QtCore.QModelIndex(), *args, **kwargs):
        return 2

    def data(self, index: QtCore.QModelIndex, role=None):
        if not index.isValid():
            return QtCore.QVariant()
        elif role == QtCore.Qt.DisplayRole:
            return self.project_table[index.row()][index.column()]

    def flags(self, index: QtCore.QModelIndex):
        if not index.isValid():
            return QtCore.QVariant()
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class ProjectTableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        QtWidgets.QTableView.__init__(self, parent)
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.setMinimumWidth(450)
        self.verticalHeader().setMinimumWidth(30)


class LoadDialog(QtWidgets.QDialog):
    # noinspection PyArgumentList
    def __init__(self, parent=None,
                 flags=QtCore.Qt.CustomizeWindowHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool):
        QtWidgets.QDialog.__init__(self, parent, flags)

        load_table_group = QtWidgets.QGroupBox(self.tr('Project List'))
        self.load_table_view = ProjectTableView()
        self.load_table_view.doubleClicked.connect(self.accept)
        load_table_layout = QtWidgets.QGridLayout()
        load_table_layout.addWidget(self.load_table_view)
        load_table_group.setLayout(load_table_layout)

        accept_button = QtWidgets.QPushButton(self.tr('Load'))
        reject_button = QtWidgets.QPushButton(self.tr('Quit'))
        button_box = QtWidgets.QDialogButtonBox()
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.addButton(accept_button, QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(reject_button, QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(load_table_group, 0, 0, 1, 1)
        main_layout.addWidget(button_box, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.setLayout(main_layout)

    def load_project(self) -> sqlite3.Connection:
        config = configparser.ConfigParser()
        config.read('config.ini')
        path = config.get('path', 'default_folder') + '/'
        project_table = []
        for file in os.listdir(path):
            if file.endswith('.db3'):
                temp_conn = sqlite3.Connection(path + file)
                c = temp_conn.cursor()
                c.execute('''SELECT [项目全称] FROM [基础信息];''')
                project_name = c.fetchone()
                project_table.append([file.replace('.db3', ''), project_name])
                c.close()
                temp_conn.close()
        project_table_model = ProjectTableModel(project_table)
        self.load_table_view.setModel(project_table_model)
        self.load_table_view.setColumnWidth(0, 80)
        self.load_table_view.setColumnWidth(1, 320)
        if len(project_table):
            self.load_table_view.setCurrentIndex(project_table_model.createIndex(0, 0))
        if self.exec_() and len(project_table):
            project_file = path + project_table[self.load_table_view.currentIndex().row()][0] + '.db3'
            return sqlite3.connect(project_file)
