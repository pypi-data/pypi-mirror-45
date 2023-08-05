# -*- coding: utf-8 -*-
'''
读取CSS用模块。
'''
from .CustomTitlebar.framelesswindow import FramelessWindow

import sys, os
from linecache import getline


class CommonHelper:

    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            # #3daee9;
            border_color = getline(style, 2).split(":")[-1].strip()[:-1]

            os.environ['border_color'] = border_color

            return f.read()

    @staticmethod
    def FrameCustomerTitle(ui, title="python", setparent=False, icon=''):
        framelessWindow = FramelessWindow(title, icon=icon)

        styleFile = os.path.join(os.path.dirname(sys.argv[0]), 'Styles/style.css')
        qssStyle = CommonHelper.readQss(styleFile)
        framelessWindow.setStyleSheet(qssStyle)

        framelessWindow.setContent(ui)

        if setparent:
            ui.setParent(framelessWindow)

        return framelessWindow
