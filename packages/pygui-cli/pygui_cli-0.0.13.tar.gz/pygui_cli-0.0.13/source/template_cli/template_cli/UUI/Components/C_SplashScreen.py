import time

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QDesktopWidget, QApplication

from Tools.BasePara import setting_path


class C_QSplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()  # 启动程序的图片
        # 效果 fade =1 淡入   fade= 2  淡出，  t sleep 时间 毫秒
        s = QSettings(setting_path, QSettings.IniFormat)

        font = QFont()
        font.setPointSize(30)
        font.setFamily("黑体")
        self.setFont(font)

        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignCenter);

        label1 = QLabel("高压电网监控" + "\n"
                        + "系统软件V1.0" + "\n" * 2,
                        self);
        label1.setAlignment(Qt.AlignCenter)

        # 公司名
        gs_name = s.value("SYSTME/gs_name", "杭州三联智能科技有限公司")
        label2 = QLabel(gs_name);

        layout.addWidget(label1)

        if s.value("SYSTEM/show_gs", True) != "false":
            layout.addWidget(label2)

        self.setLayout(layout)

    def effect(self):
        # self.showMessage("你好啊")
        self.show()
        self.center()
        self.setWindowOpacity(0)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() + 0.02  # 设置淡入
            if newOpacity > 1:
                break

            self.setWindowOpacity(newOpacity)
            # self.show()
            t -= 1
            QApplication.processEvents()
            time.sleep(0.02)

        time.sleep(0.5)
        t = 0
        while t <= 50:
            newOpacity = self.windowOpacity() - 0.02  # 设置淡出
            if newOpacity < 0:
                break

            self.setWindowOpacity(newOpacity)
            t -= 1
            QApplication.processEvents()
            time.sleep(0.01)
        self.setWindowOpacity(0)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
