#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sqlite3
from PyQt5 import QtWidgets, QtGui
from .create_dialog import CreateDialog
from .load_dialog import LoadDialog
from .option_dialog import OptionDialog
from ..branch_thread import CreateProjectThread
from ..information_widget.information_frame import InformationFrame
from ..asset_method.account_tree import AccountTree
from ..asset_method.edit_table import EditTable
from ..asset_method.input_table import InputTable
from ..asset_method.summary_table import SummaryTable
# from ..custom_widget import UnFrameWindow
from ..initialize_setting import EDIT_TABLE, SUMMARY_VIEW, SPECIAL_TABLE
from program.resource import *


class MainWindow(QtWidgets.QMainWindow):
    conn: sqlite3.Connection = None
    branch_thread = QtCore.QThread()

    def __init__(self, parent=None, flags=QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint):
        QtWidgets.QMainWindow.__init__(self, parent, flags)
        self.account_dock = QtWidgets.QDockWidget(self.tr('Account'), self, QtCore.Qt.CustomizeWindowHint)
        self.account_dock.setObjectName('Account Dock')
        self.account_dock.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures | QtWidgets.QDockWidget.DockWidgetClosable)

        create_project_action = self.create_action(self.tr('New'), self.create_project,
                                                   ':/icon/create_project.png')
        load_project_action = self.create_action(self.tr('Load'), self.load_project,
                                                 ':/icon/load_project.png')
        close_project_action = self.create_action(self.tr('Close'), self.close_project,
                                                  ':/icon/close_project.png')
        program_setting_action = self.create_action(self.tr('Setting'), self.option_setting,
                                                    ':/icon/path_setting.png')
        exit_program_action = self.create_action(self.tr('Exit'), self.close)
        project_menu = self.create_menu(self.tr('Project'), None,
                                        [create_project_action,
                                         load_project_action,
                                         close_project_action,
                                         program_setting_action,
                                         exit_program_action])

        project_information_action = self.create_action(self.tr('Project Information'), self.project_information)
        material_list_action = self.create_action(self.tr('Material List'))
        field_record_action = self.create_action(self.tr('Field Record'))
        project_contract_action = self.create_action(self.tr('Project Contract'))
        commitment_letter_action = self.create_action(self.tr('Commitment Letter'))
        service_question_action = self.create_action(self.tr('Service Question'))
        cash_check_action = self.create_action(self.tr('Cash Check'))
        current_letter_action = self.create_action(self.tr('Current Letter'))
        output_menu = self.create_menu(self.tr('Output'), None,
                                       [material_list_action,
                                        field_record_action,
                                        project_contract_action,
                                        commitment_letter_action,
                                        service_question_action,
                                        cash_check_action,
                                        current_letter_action])
        work_menu = self.create_menu(self.tr('Field Work'), None,
                                     [project_information_action,
                                      output_menu])

        asset_method_action = self.create_action(self.tr('Asset Method'), self.asset_method)
        income_method_action = self.create_action(self.tr('Income Method'))
        appraise_menu = self.create_menu(self.tr('Appraise Work'), None,
                                         [asset_method_action,
                                          income_method_action])

        appraise_report_action = self.create_action(self.tr('Appraise Report'))
        appraise_explain_action = self.create_action(self.tr('Appraise Explain'))
        declaration_form_action = self.create_action(self.tr('Declaration Form'))
        detail_form_action = self.create_action(self.tr('Detail Form'))
        work_draft = self.create_action(self.tr('Work Draft'))
        generate_menu = self.create_menu(self.tr('Generate'), None,
                                         [appraise_report_action,
                                          appraise_explain_action,
                                          declaration_form_action,
                                          detail_form_action,
                                          work_draft])

        work_staff_action = self.create_action(self.tr('Staff'))
        about_program_action = self.create_action(self.tr('About'))
        option_menu = self.create_menu(self.tr('Option'), None,
                                       [work_staff_action,
                                        about_program_action])

        self.menuBar().addMenu(project_menu)
        self.menuBar().addMenu(work_menu)
        self.menuBar().addMenu(appraise_menu)
        self.menuBar().addMenu(generate_menu)
        self.menuBar().addMenu(option_menu)

        self.toolbar: QtWidgets.QToolBar = self.addToolBar(self.tr('Toolbar'))
        self.toolbar.setIconSize(QtCore.QSize(24, 24))
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.status = QtWidgets.QStatusBar()
        self.setStatusBar(self.status)

        self.setMinimumSize(1280, 800)
        self.setWindowIcon(QtGui.QIcon(':/icon/icon.png'))
        self.setWindowTitle(self.tr('Eureka Appraise'))

        self.set_enabled(False)

    def create_project(self):
        project_file, project_code = CreateDialog().get_project_path()
        if project_file:
            self.close_project()
            if os.path.exists(project_file):
                box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', '')
                box.setWindowIcon(QtGui.QIcon(':/icon/icon.png'))
                box.setWindowTitle(self.tr('Warning'))
                box.setText(self.tr('Project file already exists!\nOverwrite?'))
                yes = box.addButton(self.tr('Confirm'), QtWidgets.QMessageBox.YesRole)
                box.addButton(self.tr('Cancel'), QtWidgets.QMessageBox.NoRole)
                box.exec_()
                if box.clickedButton() == yes:
                    os.remove(project_file)
            self.setEnabled(False)
            create_database_thread = CreateProjectThread(project_file, project_code, self)
            create_database_thread.logPrinter.connect(self.status.showMessage)
            create_database_thread.errorPrinter.connect(print)
            create_database_thread.finished.connect(self.start_project)
            create_database_thread.start()

    def load_project(self):
        conn = LoadDialog().load_project()
        if conn:
            self.conn = conn
            self.set_enabled(False)
            self.set_enabled(True)

    def close_project(self):
        if self.conn:
            c = self.conn.cursor()
            c.execute('VACUUM')
            c.close()
            self.conn.close()
            self.conn = None
        self.set_enabled(False)

    def option_setting(self):
        charge = OptionDialog().set_option()
        if charge:
            box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, '', '')
            box.setWindowTitle(self.tr('Alert'))
            box.setText(self.tr('Restart program to switch setting?'))
            yes = box.addButton(self.tr('Yes'), QtWidgets.QMessageBox.YesRole)
            box.addButton(self.tr('Wait'), QtWidgets.QMessageBox.NoRole)
            box.setWindowIcon(QtGui.QIcon(':/icon/icon.png'))
            box.exec_()
            if box.clickedButton() == yes:
                os.startfile('appraise.pyw')
                self.close()

    def project_information(self):
        information_frame = InformationFrame(self.conn, self)
        self.setCentralWidget(information_frame)

    def asset_method(self):
        account_tree = AccountTree(self.conn, self)
        self.account_dock.setWidget(account_tree)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.account_dock)
        self.account_dock.show()

    def open_account(self, index: QtCore.QModelIndex):
        table_name = index.internalPointer().data(0)
        if table_name in EDIT_TABLE:
            table = EditTable(self.conn, table_name, self)
        elif table_name in SUMMARY_VIEW:
            table = SummaryTable(self.conn, table_name, self)
        elif table_name in SPECIAL_TABLE:
            table = InputTable(self.conn, table_name, self)
        else:
            table = EditTable(self.conn, table_name, self)
        self.setCentralWidget(table)

    def start_project(self, file: str):
        self.conn = sqlite3.connect(file)
        self.set_enabled(True)
        self.setEnabled(True)

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
        self.findChild(QtWidgets.QAction, self.tr('Close')).setEnabled(enabled)
        self.findChild(QtWidgets.QMenu, self.tr('Field Work')).setEnabled(enabled)
        self.findChild(QtWidgets.QMenu, self.tr('Appraise Work')).setEnabled(enabled)
        self.findChild(QtWidgets.QMenu, self.tr('Generate')).setEnabled(enabled)
        self.findChild(QtWidgets.QMenu, self.tr('Option')).setEnabled(enabled)
        if not enabled:
            if self.account_dock:
                self.account_dock.hide()
            self.setCentralWidget(QtWidgets.QLabel())

    def closeEvent(self, event: QtCore.QEvent):
        self.close_project()
        event.accept()
