#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from PyQt5 import QtWidgets, QtGui
from .create_dialog import CreateDialog
from .load_dialog import LoadDialog
from ..branch_thread import CreateDatabaseThread
from ..custom_widget import UnFrameWindow
from resource import *


class MainWindow(UnFrameWindow):
    conn: sqlite3.Connection = None
    branch_thread = QtCore.QThread()

    def __init__(self, rect):
        UnFrameWindow.__init__(self, rect)

        self.create_project_action = self.create_action(self.tr('New'), self.create_project,
                                                        ':/icon/create_project.png')
        self.load_project_action = self.create_action(self.tr('Load'), self.load_project,
                                                      ':/icon/load_project.png')
        self.close_project_action = self.create_action(self.tr('Close'), self.close_project,
                                                       ':/icon/close_project.png')
        self.option_setting_action = self.create_action(self.tr('Option'), self.option_setting,
                                                        ':/icon/path_setting.png')
        self.exit_program_action = self.create_action(self.tr('Exit'), self.close)
        self.project_menu = self.create_menu(self.tr('Project'), None,
                                             [self.create_project_action,
                                              self.load_project_action,
                                              self.close_project_action,
                                              self.option_setting_action,
                                              self.exit_program_action])

        self.menuBar().addMenu(self.project_menu)

        self.toolbar: QtWidgets.QToolBar = self.addToolBar(self.tr('Toolbar'))
        self.toolbar.setIconSize(QtCore.QSize(24, 24))
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.setMinimumSize(800, 600)
        self.setWindowIcon(QtGui.QIcon(':/icon/icon.png'))
        self.setWindowTitle(self.tr('Eureka Appraise'))

    def create_project(self):
        project_file, project_code = CreateDialog().get_project_path()
        if project_file:
            if os.path.exists(project_file):
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', '')
                box.setWindowIcon(QtGui.QIcon(':/icon/icon.png'))
                box.setWindowTitle(self.tr('Warning'))
                box.setText(self.tr('Project file already exists!\nOverwrite?'))
                yes = box.addButton(self.tr('Confirm'), QtWidgets.QMessageBox.YesRole)
                box.addButton(self.tr('Cancel'), QtWidgets.QMessageBox.NoRole)
                box.exec_()
                if box.clickedButton() == yes:
                    self.close_project()
                    os.remove(project_file)
            self.create_database(project_file, project_code)
            self.conn = sqlite3.connect(project_file)

    def create_database(self, file, code):
        self.conn = sqlite3.connect(file)
        create_database_thread = CreateDatabaseThread(self.conn, code, self)
        create_database_thread.moveToThread(self.branch_thread)
        create_database_thread.logPrinter.connect(print)
        create_database_thread.errorPrinter.connect(print)
        create_database_thread.finished.connect(self.set_enabled)
        create_database_thread.finished.connect(self.branch_thread.quit)
        self.branch_thread.started.connect(create_database_thread.work)
        self.branch_thread.start()

    def load_project(self):
        conn = LoadDialog().load_project()
        if conn:
            self.conn = conn

    def close_project(self):
        if self.conn:
            c = self.conn.cursor()
            c.execute('VACUUM')
            c.close()
            self.conn.close()
            self.conn = None

    def option_setting(self):
        pass

    def create_action(self, name: str, slot: classmethod = None, icon: str = None) -> QtWidgets.QAction:
        action = QtWidgets.QAction(name, self)
        action.setObjectName(name)
        if slot:
            action.triggered.connect(slot)
        if icon:
            action.setIcon(QtGui.QIcon(icon))
        return action

    def create_menu(self, name: str, icon: str = None, child_objects: iter = None) -> QtWidgets.QMenu:
        menu = QtWidgets.QMenu(name, self)
        menu.setObjectName(name)
        if icon:
            menu.setIcon(QtGui.QIcon(icon))
        if child_objects:
            for child_object in child_objects:
                if isinstance(child_object, QtWidgets.QAction):
                    menu.addAction(child_object)
                elif isinstance(child_object, QtWidgets.QMenu):
                    menu.addMenu(child_object)
                elif child_object is None:
                    menu.addSeparator()
        return menu

    def set_enabled(self, enabled: bool = True):
        self.close_project_action.setEnabled(enabled)

    def closeEvent(self, event):
        self.close_project()
        event.accept()
