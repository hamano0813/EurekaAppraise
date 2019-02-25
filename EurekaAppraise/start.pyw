#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import configparser
import locale
from PyQt5 import QtWidgets
from resource import *

config = configparser.ConfigParser()

if os.path.exists('config.ini'):
    config.read('config.ini')
    language = config.get('setting', 'language')
    style = config.get('setting', 'style')
    path = config.get('path', 'default_folder')
else:
    config.add_section('setting')
    language = locale.getdefaultlocale()[0]
    style = 'light'
    path = None
    config.set('setting', 'language', language)
    config.set('setting', 'style', style)
    config.add_section('path')
    config.set('path', 'default_folder', '')
    config.write(open('config.ini', 'w'))

app = QtWidgets.QApplication(sys.argv)

translator = QtCore.QTranslator()
translator.load(f':/qm/{language}')
app.installTranslator(translator)

style_file = QtCore.QFile(f':/qss/{style}.qss')
style_file.open(QtCore.QFile.ReadOnly)
stylesheet = bytearray(style_file.readAll()).decode('UTF-8')
app.setStyleSheet(stylesheet)


class InitializeFolder(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        global path, config
        if not path:
            self.dialog = QtWidgets.QFileDialog()
            self.dialog.setWindowTitle(self.tr('Select default folder'))
            self.dialog.setDirectory('C:/')
            path = self.dialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)
            if path:
                config.set('path', 'default_folder', path)
                config.write(open('config.ini', 'w'))
            else:
                self.box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '', '')
                self.box.setWindowTitle(self.tr('Error'))
                self.box.setText(self.tr('Must choose folder!'))
                self.box.addButton(self.tr('Close'), QtWidgets.QMessageBox.NoRole)
                self.box.exec_()
                sys.exit()
        elif not os.path.exists(path):
            os.mkdir(path)


InitializeFolder()

sys.exit(app.exec_())
