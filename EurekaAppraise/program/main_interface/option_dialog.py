#!/usr/bin/env python
# -*- coding: utf-8 -*-

import locale
import configparser
from PyQt5 import QtWidgets, QtCore


class OptionDialog(QtWidgets.QDialog):
    # noinspection PyArgumentList
    def __init__(self, parent=None,
                 flags=QtCore.Qt.CustomizeWindowHint | QtCore.Qt.MSWindowsFixedSizeDialogHint | QtCore.Qt.Tool):
        QtWidgets.QDialog.__init__(self, parent, flags)

        path_group = QtWidgets.QGroupBox(self.tr('Default Folder Setting'))
        self.path_line = QtWidgets.QLineEdit()
        self.path_line.setReadOnly(True)
        path_button = QtWidgets.QPushButton(self.tr('Select'))
        path_layout = QtWidgets.QGridLayout()
        path_layout.addWidget(self.path_line, 0, 0, 1, 1)
        path_layout.addWidget(path_button, 0, 1, 1, 1)
        path_group.setLayout(path_layout)
        path_button.clicked.connect(self.set_path)

        language_group = QtWidgets.QGroupBox(self.tr('Language Switch (after restart)'))
        self.zh_cn_radio = QtWidgets.QRadioButton('中文')
        self.en_us_radio = QtWidgets.QRadioButton('English')
        language_layout = QtWidgets.QGridLayout()
        language_layout.addWidget(self.zh_cn_radio, 0, 0, 1, 1)
        language_layout.addWidget(self.en_us_radio, 0, 1, 1, 1)
        language_group.setLayout(language_layout)
        language_group.setMinimumWidth(200)

        language_button = QtWidgets.QButtonGroup()
        language_button.addButton(self.zh_cn_radio, 1)
        language_button.addButton(self.en_us_radio, 2)

        style_group = QtWidgets.QGroupBox(self.tr('Style Switch (after restart)'))
        self.light_radio = QtWidgets.QRadioButton(self.tr('Light'))
        self.dark_radio = QtWidgets.QRadioButton(self.tr('Dark'))
        style_layout = QtWidgets.QGridLayout()
        style_layout.addWidget(self.light_radio, 0, 0, 1, 1)
        style_layout.addWidget(self.dark_radio, 0, 1, 1, 1)
        style_group.setLayout(style_layout)
        style_group.setMinimumWidth(200)

        style_button = QtWidgets.QButtonGroup()
        style_button.addButton(self.light_radio, 1)
        style_button.addButton(self.dark_radio, 2)

        accept_button = QtWidgets.QPushButton(self.tr('Confirm'))
        reject_button = QtWidgets.QPushButton(self.tr('Cancel'))
        button_box = QtWidgets.QDialogButtonBox()
        button_box.setOrientation(QtCore.Qt.Horizontal)
        button_box.addButton(accept_button, QtWidgets.QDialogButtonBox.AcceptRole)
        button_box.addButton(reject_button, QtWidgets.QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(path_group, 0, 0, 1, 2)
        main_layout.addWidget(language_group, 1, 0, 1, 1)
        main_layout.addWidget(style_group, 1, 1, 1, 1)
        main_layout.addWidget(button_box, 2, 0, 1, 2, QtCore.Qt.AlignRight)
        self.setLayout(main_layout)

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.language = config.get('setting', 'language')
        if self.language == 'zh_CN':
            self.zh_cn_radio.setChecked(True)
        elif self.language == 'en_US':
            self.en_us_radio.setChecked(True)
        self.style = config.get('setting', 'style')
        if self.style == 'light':
            self.light_radio.setChecked(True)
        elif self.style == 'dark':
            self.dark_radio.setChecked(True)
        path = config.get('path', 'default_folder')
        self.path_line.setText(path)

    def set_path(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setWindowTitle(self.tr('Select default folder'))
        dialog.setDirectory(self.path_line.text())
        path = dialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)
        if path:
            self.path_line.setText(path)

    def set_option(self):
        if self.exec_():
            config = configparser.ConfigParser()
            config.read('config.ini')
            config.set('path', 'default_folder', self.path_line.text())
            if self.zh_cn_radio.isChecked():
                language = 'zh_CN'
            elif self.en_us_radio.isChecked():
                language = 'en_US'
            else:
                language = locale.getdefaultlocale()[0]
            if self.dark_radio.isChecked():
                style = 'dark'
            else:
                style = 'light'
            config.set('setting', 'language', language)
            config.set('setting', 'style', style)
            config.write(open('config.ini', 'w'))
            if self.language == language and self.style == style:
                return False
            else:
                return True
