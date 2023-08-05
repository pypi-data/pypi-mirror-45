from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QStackedWidget, QWidget

"""
custom yourself function that be add to MainWindow.
"""


def fm_returnTo(self: QWidget, toIndex: int, stackedWidget=None):
    """用于页面跳转"""
    if stackedWidget is None:
        if hasattr(self, "stackedWidget"):
            stackedWidget = self.stackedWidget
        else:
            return
    else:
        stackedWidget.setCurrentIndex(toIndex)


class FuncMixin(QObject):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        # globals().items() => key:(functionName,build_func)
        all_fm = [(func[0], func[1]) for k, func in enumerate(globals().items()) if func[0].find('fm') != -1]
        for f in all_fm:
            funcName, func = f
            setattr(self, funcName, func)
