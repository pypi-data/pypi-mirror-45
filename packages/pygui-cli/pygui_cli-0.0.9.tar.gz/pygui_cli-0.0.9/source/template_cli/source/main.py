# -*- coding: utf-8 -*-
"""
main .
"""

import io, sys

sys.path.append('./Styles/CustomTitlebar')
# use catch error
import traceback, faulthandler

from Tools.main_setting import SettingInfo

"""
Created on 2018-09-16 <br>
description: $description$ <br>
author: 625781186@qq.com <br>
site: https://github.com/625781186 <br>
更多经典例子:https://github.com/892768447/PyQt <br>
课件: https://github.com/625781186/WoHowLearn_PyQt5 <br>
视频教程: https://space.bilibili.com/1863103/#/ <br>
"""
from Styles.CommonHelper import CommonHelper
from Tools.FuncMixin import FuncMixin
from Tools.LogError import logger
from UUI.Components.C_SplashScreen import C_QSplashScreen
from UUI.Components.C_Application import C_QSingleApplication
from main_preinit_ui import Ui_initUI, QStyleFactory, \
    QApplication, QMessageBox, Qt, QPushButton


# from PluginManager.PluginManager import PluginManager


class MainWindow(Ui_initUI, FuncMixin, SettingInfo):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        # -------------quick get/set mwObj------------- ↓
        from Tools import BasePara
        BasePara.mw = self
        BasePara.settings = self.settings
        # -------------quick get/set mwObj------------- ↑

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self._initUI()
        self.restoreSettings()
        # using test logging
        # self.btn = QPushButton("test logging", self, clicked=lambda: print(1 + "xxx"))
        # self.layout().addWidget(self.btn)


    # def closeEvent(self, e):
    #     # This is invalid.
    #     # please goto Tools.main_setting.py edit m_closeEvent
    #     print("This is invalid")
    #     return super().closeEvent(e)


def main(style=1):
    # style1
    app.setStyle(QStyleFactory.create("Fusion"))

    global ui
    ui = MainWindow()

    if style == 1:
        ui.show()
        # ui.showMaximized()

    # style3
    elif style == 3:

        # 自定义边框
        framelessWindow = \
            CommonHelper.FrameCustomerTitle(ui,
                                            title="Wow",
                                            icon=":/button_Ima/git.ico")
        # styleFile = './Style/style.css'
        # qssStyle = CommonHelper.readQss(styleFile)
        # framelessWindow.setStyleSheet(qssStyle)
        framelessWindow.show()
    elif style == 2:
        pass
        # style2
        # If you want to use this style, please pip install qdarkstyle.
        # import qdarkstyle
        # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


def pageMain(style=1):
    # Using StackedWidget Debug
    main(style)
    # ui.returnTo(0)


if __name__ == "__main__":

    # ------------- globals catch error ------------- ↓
    def excepthook(excType, excValue, tracebackobj):
        """ globals catch error / tb = traceback"""
        try:
            errmsg = '{0}: \n{1}'.format(str(excType), str(excValue))

            tbinfofile = io.StringIO()
            traceback.print_tb(tracebackobj, None, tbinfofile)
            tbinfofile.seek(0)

            tbinfo = tbinfofile.read()

            logger.warning(errmsg + tbinfo)

            faulthandler.enable(file=sys.stderr)
        except:
            pass
        sys.__excepthook__(excType, excValue, tracebackobj)


    sys.excepthook = excepthook


    # ------------- globals catch error ------------- ↑

    # ------------- app -> splash -> pageMain -> main ------------- ↓

    def showSplashScreen(mainfun, needSignal=False, needShowSplash=False, style=1):
        """
        start 启动界面"

        :param mainfun: main()
        :param needSignal: only one app
        :param needShowSplash:
        :param style: 1:default ; 2:qdarkstyle; 3.unlesswindow
        :return:
        """
        global app
        app = QApplication(sys.argv) if needSignal is False else C_QSingleApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)

        # -------------judge singleApp ------------- ↓
        if needSignal is True and app.isRunning():
            app.sendMessage("app is running")
            QMessageBox.warning(None, "警告", "已启动软件, 请结束上一次启动的软件后再运行！")
            sys.exit(0)
        # -------------judge singleApp ------------- ↑

        if needShowSplash is True:
            splash = C_QSplashScreen()
            splash.effect()
            app.processEvents()
            mainfun(style)
            splash.finish(ui)
        else:
            mainfun(style)
        app.setActivationWindow(ui) if needSignal is True else None


    showSplashScreen(pageMain,
                     needSignal=False,
                     needShowSplash=False,
                     style=3)
    # ------------- app -> splash -> pageMain -> main ------------- ↑

    sys.exit(app.exec_())
