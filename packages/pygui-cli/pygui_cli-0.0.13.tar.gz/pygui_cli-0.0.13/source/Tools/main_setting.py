import os
from collections import OrderedDict

from PyQt5.QtCore import QStandardPaths, QObject, QSettings
from PyQt5.QtWidgets import qApp

from Tools.BasePara import setting_path


# from Tools.create_lnk import create_to_StartUp


class SettingInfo(QObject):
    settings = QSettings(setting_path, QSettings.IniFormat)

    def __init__(self, parent=None):
        super().__init__(parent)

        ########################################Settings

        # settings.beginGroup('UserInterface')  # 开始一个新的组
        # settings.setValue('window-width', 600)
        # settings.setValue('window-height', 300)
        # settings.endGroup()  # 结束这个分组

    def restoreSettings(self):
        s = self.settings
        try:
            # 首测运行初始化 ， 需要右键管理员身份运行
            appName = qApp.applicationFilePath().split(r"/")[-1] + ".lnk"
            startapp = QStandardPaths.standardLocations(QStandardPaths.DesktopLocation)[0]
            global target_path
            target_path = os.path.join(startapp, appName)

            # print(qApp.applicationFilePath(), target_path, )
            # create_to_StartUp(qApp.applicationFilePath(), target_path)
        except:
            import traceback
            print(traceback.format_exc())
        try:
            # 主窗体 尺寸位置
            self.restoreState(s.value("window_info/windowState"))
            self.restoreGeometry(s.value("window_info/geometry"))

        except:
            pass
        # settings.setValue("windowState", self.saveState());

    def closeEvent(self, e):
        """

        :param e:
        :param args:
        :param kwargs:
        :return:
        """
        print("close")

        # 主窗体 尺寸位置
        self.settings.setValue("window_info/windowState", self.saveState());
        self.settings.setValue("window_info/geometry", self.saveGeometry());

        DEBUG_SEC = self.settings.value("DEBUG/DEBUG_SEC", 6000)
        self.settings.setValue("DEBUG/DEBUG_SEC", DEBUG_SEC)

        # return super().closeEvent(e)
        ## 安全退出线程
        # self.realtime_data_thread.terminate()
        # self.breakThread_signal.emit(True)
        # self.alarmRecord_tv.closeDB()
