## python main file to run the program


# coding:utf-8
import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from app.view.main_window import MainWindow

script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

app = QApplication(sys.argv)
# create main window
w = MainWindow()
w.show()

sys.exit(app.exec_())