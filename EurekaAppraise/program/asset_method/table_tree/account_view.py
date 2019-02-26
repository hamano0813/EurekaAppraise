#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from .account_tree import ACCOUNT_TREE
from .account_model import AccountModel


class AccountView(QtWidgets.QTreeView):
    def __init__(self, conn, parent=None):
        super(AccountView, self).__init__(parent)
        self.header().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.setExpandsOnDoubleClick(False)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # self.horizontalScrollBar().setStyleSheet('QScrollBar:horizontal{height:0px;}')
        account_model = AccountModel(conn, ACCOUNT_TREE)
        self.setModel(account_model)
