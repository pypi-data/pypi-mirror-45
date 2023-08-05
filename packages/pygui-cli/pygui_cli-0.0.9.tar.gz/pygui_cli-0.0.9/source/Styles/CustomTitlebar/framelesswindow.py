# -*- coding: utf-8 -*-

"""
Module implementing FramelessWindow.
"""

import sip, os
# import configparser #You need pip install configparser
from PyQt5.QtCore import Qt, pyqtSlot, QTimer, QRect
from PyQt5.QtGui import QIcon, QCursor, QPainter, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QApplication, QMenu, QHBoxLayout, QWidget, QMainWindow

from .Ui_framelesswindow import Ui_FramelessWindow

PADDING = 4


class FramelessWindow(QWidget, Ui_FramelessWindow):
    subUI = None

    def __init__(self, title="python", parent=None, icon=''):
        super(FramelessWindow, self).__init__(parent, Qt.FramelessWindowHint)
        self.setupUi(self)
        self._icon = icon
        #        self.setMouseTracking(True)
        self.setTitle(title)

        self.icon = icon if icon != "" else ":/button_Ima/git.ico"

        self.contentLayout = QHBoxLayout(self.windowContent)

        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明

        self.windowTitlebar.setAttribute(Qt.WA_StyledBackground, True)

        self.restoreButton.setVisible(False)
        # ================== 托盘图标 ==================#
        self.tray_icon = QIcon(self.icon)  # 创建图标

        self.tray = QSystemTrayIcon(self)  # 创建系统托盘对象
        self.tray.setIcon(self.tray_icon)  # 设置系统托盘图标

        self.MaxAction = QAction(u'最大化 ', self,
                                 triggered=lambda: self.setWindowState(Qt.WindowMaximized))  # 添加一级菜单动作选项(最大化主窗口)
        self.RestoreAction = QAction(u'还原 ', self, triggered=self.show)  # 添加一级菜单动作选项(还原主窗口)
        self.QuitAction = QAction(u'退出 ', self, triggered=self.close)  # 添加一级菜单动作选项(退出程序)

        self.tray_menu = QMenu(QApplication.desktop())  # 创建菜单
        self.tray_menu.addAction(self.MaxAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.RestoreAction)  # 为菜单添加动作
        self.tray_menu.addAction(self.QuitAction)

        self.tray.setContextMenu(self.tray_menu)  # 设置系统托盘菜单
        self.tray.show()

        # =================== 无 窗 体 拉 伸 ===================↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # 设置widget鼠标跟踪   
        self.setMouseTracking(True)
        # 边框距离
        self.SHADOW_WIDTH = 0
        # 鼠标左键是否按下
        self.isLeftPressDown = False
        # 拖动时坐标
        self.dragPosition = 0
        # 枚举参数
        self.Numbers = self.enum(
            UP=0, DOWN=1, LEFT=2, RIGHT=3, LEFTTOP=4,
            LEFTBOTTOM=5, RIGHTBOTTOM=6, RIGHTTOP=7, NONE=8
        )
        # 初始鼠标状态
        self.dir = self.Numbers.NONE

    def enum(self, **enums):
        return type('Enum', (), enums)

    def region(self, cursorGlobalPoint):
        # 获取窗体在屏幕上的位置区域，
        # tl为topleft点，
        # rb为rightbottom点
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        x = cursorGlobalPoint.x()
        y = cursorGlobalPoint.y()

        if (tl.x() + PADDING >= x
                and tl.x() <= x
                and tl.y() + PADDING >= y
                and tl.y() <= y):
            # 左上角
            self.dir = self.Numbers.LEFTTOP
            self.setCursor(QCursor(Qt.SizeFDiagCursor))  # 设置鼠标形状
        elif (x >= rb.x() - PADDING
              and x <= rb.x()
              and y >= rb.y() - PADDING
              and y <= rb.y()):
            # 右下角
            self.dir = self.Numbers.RIGHTBOTTOM
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif (x <= tl.x() + PADDING
              and x >= tl.x()
              and y >= rb.y() - PADDING
              and y <= rb.y()):
            # 左下角
            self.dir = self.Numbers.LEFTBOTTOM
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif (x <= rb.x()
              and x >= rb.x() - PADDING
              and y >= tl.y()
              and y <= tl.y() + PADDING):
            # 右上角
            self.dir = self.Numbers.RIGHTTOP
            self.setCursor(QCursor(Qt.SizeBDiagCursor))

        elif (x <= tl.x() + PADDING and x >= tl.x()):
            # 左边
            self.dir = self.Numbers.LEFT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif (x <= rb.x() and x >= rb.x() - PADDING):
            # 右边

            self.dir = self.Numbers.RIGHT
            self.setCursor(QCursor(Qt.SizeHorCursor))
        elif (y >= tl.y() and y <= tl.y() + PADDING):
            # 上边
            self.dir = self.Numbers.UP
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif (y <= rb.y() and y >= rb.y() - PADDING):
            # 下边
            self.dir = self.Numbers.DOWN
            self.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            # 默认
            self.dir = self.Numbers.NONE
            self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = False
            if (self.dir != self.Numbers.NONE):
                QTimer.singleShot(300, self.releaseMouse)
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.isLeftPressDown = True
            if (self.dir != self.Numbers.NONE):
                QTimer.singleShot(300, self.mouseGrabber)

            else:
                self.dragPosition = event.globalPos() \
                                    - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        gloPoint = event.globalPos()
        rect = self.rect()
        tl = self.mapToGlobal(rect.topLeft())
        rb = self.mapToGlobal(rect.bottomRight())

        if (not self.isLeftPressDown):
            self.region(gloPoint)
        else:
            if (self.dir != self.Numbers.NONE):
                rmove = QRect(tl, rb)
                if (self.dir == self.Numbers.LEFT):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                elif (self.dir == self.Numbers.RIGHT):

                    rmove.setWidth(gloPoint.x() - tl.x())
                elif (self.dir == self.Numbers.UP):
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.DOWN):
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.LEFTTOP):
                    if (rb.x() - gloPoint.x() <= self.minimumWidth()):
                        rmove.setX(tl.x())
                    else:
                        rmove.setX(gloPoint.x())
                    if (rb.y() - gloPoint.y() <= self.minimumHeight()):
                        rmove.setY(tl.y())
                    else:
                        rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.RIGHTTOP):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setY(gloPoint.y())
                elif (self.dir == self.Numbers.LEFTBOTTOM):
                    rmove.setX(gloPoint.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                elif (self.dir == self.Numbers.RIGHTBOTTOM):
                    rmove.setWidth(gloPoint.x() - tl.x())
                    rmove.setHeight(gloPoint.y() - tl.y())
                else:
                    pass

                self.setGeometry(rmove)
            else:
                try:
                    self.move(event.globalPos() - self.dragPosition)
                except:
                    pass
                event.accept()

    # =================== 无 窗 体 拉 伸 ===================↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

    @pyqtSlot()
    def on_applicationStateChanged(state):
        pass

    @pyqtSlot()
    def on_windowTitlebar_doubleClicked(self):
        if (self.windowState() == Qt.WindowNoState):
            self.on_maximizeButton_clicked()

        elif (self.windowState() == Qt.WindowMaximized):
            self.on_restoreButton_clicked()

    @pyqtSlot()
    def on_minimizeButton_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @pyqtSlot()
    def on_restoreButton_clicked(self):
        self.restoreButton.setVisible(False)
        self.maximizeButton.setVisible(True)
        self.setWindowState(Qt.WindowNoState)

    @pyqtSlot()
    def on_maximizeButton_clicked(self):
        self.restoreButton.setVisible(True)
        self.maximizeButton.setVisible(False)
        self.setWindowState(Qt.WindowMaximized)

    @pyqtSlot()
    def on_closeButton_clicked(self):

        self.close()
        #        qApp.quit()
        try:
            sip.delete(self.tray)
        except:
            pass

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):

        self._icon = self.setIcon(value)

    def setIcon(self, icon: str):
        if isinstance(icon, QIcon):
            self.titleIconBtn.setIcon(icon)
            return icon
        elif isinstance(icon, str):

            icon_ico = QIcon()
            icon_ico.addPixmap(QPixmap(icon),
                               QIcon.Normal, QIcon.Off)
            self.titleIconBtn.setIcon(icon_ico)
            return icon_ico
        else:
            raise Exception("icon need type str or QIcon")

    def setTitle(self, text):
        self.titleText.setText(text)

    def paintEvent(self, e):
        """titlebar background color """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)  # 反锯齿
        # 外边框 颜色
        # painter.setBrush(QBrush(QColor(85, 170, 255)))
        hex_color = os.getenv('border_color')

        painter.setBrush(QBrush(QColor(hex_color)))
        painter.setPen(Qt.transparent)
        rect = self.rect()
        rect.setWidth(rect.width())
        rect.setHeight(rect.height())
        painter.drawRoundedRect(rect, 4, 4)

    def setContent(self, w):
        """
        add Window to self.contentLayout

        :param w:QWidget
        :return:
        """
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)

        self.contentLayout.addWidget(w)
        self.windowContent.setLayout(self.contentLayout)

        self.subUI = w
        self.subUI.origin_enterEvent = self.subUI.enterEvent
        self.subUI.enterEvent = self.m_enterEvent

    # def enterEvent(self, event):
    #     "have bug "
    #     return super(QWidget, self.subUI).enterEvent(event)

    def m_enterEvent(self, e):
        """
        redirect to MainWindow's enterEvent
        重定向到 MainWindow's enterEvent
        """
        self.dir = self.Numbers.NONE
        self.setCursor(QCursor(Qt.ArrowCursor))

        return self.subUI.origin_enterEvent(e)

    def closeEvent(self, event):
        """
        redirect to MainWindow's closeEvent
        重定向到 MainWindow's closeEvent
        """

        self.setWindowFlags(Qt.Widget)

        self.tray.setVisible(False)
        sip.delete(self.tray)
        return super(QWidget, self.subUI).closeEvent(event)
