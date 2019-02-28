#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui, QtCore

TITLE_HEIGHT = ICON_WIDTH = 32
BORDER_WIDTH = 3
BUTTON_WIDTH = 40


class TitleLabel(QtWidgets.QLabel):
    def __init__(self, *args):
        QtWidgets.QLabel.__init__(self, *args)
        self.setAlignment(QtCore.Qt.AlignHCenter)
        self.setFixedHeight(TITLE_HEIGHT)
        self.setIndent(10)


class IconLabel(TitleLabel):
    def __init__(self, *args):
        TitleLabel.__init__(self, *args)
        self.setFixedWidth(ICON_WIDTH)
        self.setMargin(4)

    def set_icon(self, icon: QtGui.QIcon):
        pixmap = icon.pixmap(ICON_WIDTH - 8, ICON_WIDTH - 8)
        self.setPixmap(pixmap)


class TitleButton(QtWidgets.QPushButton):
    def __init__(self, *args):
        QtWidgets.QPushButton.__init__(self, *args)
        self.setFixedWidth(BUTTON_WIDTH)


class UnFrameWindow(QtWidgets.QWidget):
    # noinspection PyArgumentList
    def __init__(self, rect: QtCore.QRect):
        super(UnFrameWindow, self).__init__(None, QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.used_rect = rect
        self.normal_rect = rect

        self.is_maximized = False
        self.move_drag_position = 0
        self._move_drag = self._corner_drag = self._bottom_drag = self._right_drag = False
        self._right_rect = self._bottom_rect = self._corner_rect = []

        icon_label = IconLabel(self)
        icon_label.setObjectName('Icon')
        icon_label.setMouseTracking(True)
        icon_label.move(BORDER_WIDTH + 1, BORDER_WIDTH)
        self.setWindowIcon = self._set_icon(self.setWindowIcon)

        title_label = TitleLabel(self)
        title_label.setObjectName('Title')
        title_label.setMouseTracking(True)
        title_label.move(ICON_WIDTH + BORDER_WIDTH + 1, BORDER_WIDTH)
        self.setWindowTitle = self._set_title(self.setWindowTitle)

        min_button = TitleButton(b'\xef\x80\xb0'.decode('utf-8'), self)
        min_button.setWhatsThis('MinMaxButton')
        min_button.setObjectName('MinButton')
        min_button.setToolTip('最小化')
        min_button.setMouseTracking(True)
        min_button.setFixedHeight(TITLE_HEIGHT)
        min_button.clicked.connect(self.showMinimized)

        max_button = TitleButton(b'\xef\x80\xb1'.decode('utf-8'), self)
        max_button.setWhatsThis('MinMaxButton')
        max_button.setObjectName('MaxButton')
        max_button.setToolTip('最大化')
        max_button.setMouseTracking(True)
        max_button.setFixedHeight(TITLE_HEIGHT)
        max_button.clicked.connect(self.charge_window)

        close_button = TitleButton(b'\xef\x81\xb2'.decode('utf-8'), self)
        close_button.setWhatsThis('CloseButton')
        close_button.setObjectName('CloseButton')
        close_button.setToolTip('关闭窗口')
        close_button.setMouseTracking(True)
        close_button.setFixedHeight(TITLE_HEIGHT)
        close_button.clicked.connect(self.close)

        self.main_window = QtWidgets.QMainWindow(None, QtCore.Qt.FramelessWindowHint)
        self.main_window.setMouseTracking(True)

        main_layout = QtWidgets.QGridLayout()
        main_layout.setContentsMargins(BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH)
        main_layout.setSpacing(0)
        main_layout.addWidget(icon_label, 0, 0, 1, 1)
        main_layout.addWidget(title_label, 0, 1, 1, 1)
        main_layout.addWidget(min_button, 0, 2, 1, 1)
        main_layout.addWidget(max_button, 0, 3, 1, 1)
        main_layout.addWidget(close_button, 0, 4, 1, 1)
        main_layout.addWidget(self.main_window, 1, 0, 1, 5)

        self.setLayout(main_layout)
        self.setMinimumSize = self._set_size(self.setMinimumSize)
        self.setMinimumSize(320, 240)
        self.setMouseTracking(True)

    def __getattr__(self, attr):
        if attr in ('menuBar', 'addToolBar', 'setStatusBar', 'setCentralWidget', 'centralWidget', 'addDockWidget'):
            return getattr(self.main_window, attr)
        else:
            return getattr(self, attr)

    def _set_size(self, func):
        def wrapper(*args):
            width, height = args
            self.normal_rect = QtCore.QRect(self.used_rect.x() + (self.used_rect.width() - width) // 2,
                                            self.used_rect.y() + (self.used_rect.height() - height) // 2,
                                            width, height)
            return func(*args)

        return wrapper

    def _set_title(self, func):
        def wrapper(*args):
            self.findChild(TitleLabel, 'Title').setText(*args)
            return func(*args)

        return wrapper

    def _set_icon(self, func):
        def wrapper(*args):
            self.findChild(IconLabel, 'Icon').set_icon(*args)
            return func(*args)

        return wrapper

    def charge_window(self):
        button: TitleButton = self.findChild(TitleButton, 'MaxButton')
        if button.text() == b'\xef\x80\xb2'.decode('utf-8'):
            self.setGeometry(self.normal_rect)
            button.setText(b'\xef\x80\xb1'.decode('utf-8'))
            button.setToolTip('最大化')
            self.is_maximized = False
        else:
            max_rect = QtCore.QRect(self.used_rect.x() - BORDER_WIDTH, self.used_rect.y() - BORDER_WIDTH,
                                    self.used_rect.width() + BORDER_WIDTH * 2,
                                    self.used_rect.height() + BORDER_WIDTH * 2)
            self.setGeometry(max_rect)
            button.setText(b'\xef\x80\xb2'.decode('utf-8'))
            button.setToolTip('恢复')
            self.is_maximized = True

    def resizeEvent(self, event: QtGui.QResizeEvent):
        self.findChild(TitleLabel, 'Title').setFixedWidth(self.width() - BORDER_WIDTH * 2 - ICON_WIDTH)
        self._right_rect = [QtCore.QPoint(x, y) for x in range(self.width() - BORDER_WIDTH, self.width() + 1)
                            for y in range(1, self.height() - BORDER_WIDTH)]
        self._bottom_rect = [QtCore.QPoint(x, y) for x in range(1, self.width() - BORDER_WIDTH)
                             for y in range(self.height() - BORDER_WIDTH, self.height() + 1)]
        self._corner_rect = [QtCore.QPoint(x, y) for x in range(self.width() - BORDER_WIDTH, self.width() + 1)
                             for y in range(self.height() - BORDER_WIDTH, self.height() + 1)]

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        if (event.button() == QtCore.Qt.LeftButton) and (event.y() < TITLE_HEIGHT + BORDER_WIDTH):
            self.charge_window()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._corner_rect):
            self._corner_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._right_rect):
            self._right_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.pos() in self._bottom_rect):
            self._bottom_drag = True
            event.accept()
        elif (event.button() == QtCore.Qt.LeftButton) and (event.y() < TITLE_HEIGHT + BORDER_WIDTH):
            self._move_drag = True
            event.accept()
        self.move_drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        if event.pos() in self._corner_rect:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif event.pos() in self._bottom_rect:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif event.pos() in self._right_rect:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
        if self._right_drag:
            self.resize(event.pos().x(), self.height())
            self.normal_rect = self.geometry()
            event.accept()
        elif self._bottom_drag:
            self.resize(self.width(), event.pos().y())
            self.normal_rect = self.geometry()
            event.accept()
        elif self._corner_drag:
            self.resize(event.pos().x(), event.pos().y())
            self.normal_rect = self.geometry()
            event.accept()
        elif self._move_drag and not self.is_maximized:
            self.move(event.globalPos() - self.move_drag_position)
            self.normal_rect = self.geometry()
            event.accept()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        self._move_drag = self._corner_drag = self._bottom_drag = self._right_drag = False

    def draw_shadow(self, painter):
        borders = [':border/border-left-top.png', ':border/border-left-bottom.png',
                   ':border/border-right-top.png', ':border/border-right-bottom.png',
                   ':border/border-top.png', ':border/border-bottom.png',
                   ':border/border-left.png', ':border/border-right.png']

        painter.drawPixmap(0, 0, BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[0]))
        painter.drawPixmap(self.width() - BORDER_WIDTH, 0, BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[2]))
        painter.drawPixmap(0, self.height() - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[1]))
        painter.drawPixmap(self.width() - BORDER_WIDTH, self.height() - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[3]))
        painter.drawPixmap(0, BORDER_WIDTH, BORDER_WIDTH, self.height() - 2 * BORDER_WIDTH,
                           QtGui.QPixmap(borders[6]).scaled(BORDER_WIDTH, self.height() - 2 * BORDER_WIDTH))
        painter.drawPixmap(self.width() - BORDER_WIDTH, BORDER_WIDTH, BORDER_WIDTH, self.height() - 2 * BORDER_WIDTH,
                           QtGui.QPixmap(borders[7]).scaled(BORDER_WIDTH, self.height() - 2 * BORDER_WIDTH))
        painter.drawPixmap(BORDER_WIDTH, 0, self.width() - 2 * BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[4]).scaled(self.width() - 2 * BORDER_WIDTH, BORDER_WIDTH))
        painter.drawPixmap(BORDER_WIDTH, self.height() - BORDER_WIDTH, self.width() - 2 * BORDER_WIDTH, BORDER_WIDTH,
                           QtGui.QPixmap(borders[5]).scaled(self.width() - 2 * BORDER_WIDTH, BORDER_WIDTH))

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        self.draw_shadow(painter)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.white)
        rect = QtCore.QRect(BORDER_WIDTH, BORDER_WIDTH, self.width() - 2 * BORDER_WIDTH,
                            self.height() - 2 * BORDER_WIDTH)
        painter.drawRect(rect)
