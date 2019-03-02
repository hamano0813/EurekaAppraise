#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from ...option_setting import ACCOUNT_TREE
from .account_model import AccountModel


class AccountTree(QtWidgets.QTreeView):
    def __init__(self, conn, parent=None):
        super(AccountTree, self).__init__(parent)
        self.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.setExpandsOnDoubleClick(False)
        self.horizontalScrollBar().setStyleSheet('QScrollBar:horizontal{height:0px;}')
        account_model = AccountModel(conn, ACCOUNT_TREE)
        self.setModel(account_model)
        self.doubleClicked[QtCore.QModelIndex].connect(self.parent().open_account)
        self.setColumnWidth(0, 130)
        self.setColumnWidth(1, 280)
        self.setFixedWidth(432)
        self.expandAll()
