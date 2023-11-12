# coding: utf-8
import os

from PyQt5.QtCore import QUrl, QSize, QCoreApplication
from PyQt5.QtGui import QIcon, QDesktopServices, QFontDatabase
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from .todo_interface import TodoInterface
from ..common.config import cfg
from ..common.style_sheet import StyleSheet

class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.todoInterface = TodoInterface(self)
        # self.connectSignalToSlot()
        self.initNavigation()
        # print(QCoreApplication.applicationDirPath() )
        font_id = QFontDatabase.addApplicationFont('app/resource/fonts/LXGWWenKaiMono-Regular.ttf')
        # print(font_id)
    def initWindow(self):
        self.resize(900, 900)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon("app/resource/images/logo.ico"))
        self.setWindowTitle('Todo List')
        # StyleSheet.HOME_INTERFACE.apply(self)
        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
    def initNavigation(self):
        # add navigation items
        self.addSubInterface(self.todoInterface, FIF.CHECKBOX, self.tr('Todo'))
        