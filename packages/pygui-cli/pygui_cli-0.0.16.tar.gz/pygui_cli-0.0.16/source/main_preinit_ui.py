# -*- coding: utf-8 -*-

"""
init UI class.
"""


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


try:
    from Ui_main import Ui_MainWindow
except ImportError as e:
    print("--1 --", e)
    try:
        from .Ui_main import Ui_MainWindow
    except ImportError as e:
        print("--2 --", e)

from Tools.BasePara import *


class Ui_initUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _initUI(self):
        """initUI"""
        pass
