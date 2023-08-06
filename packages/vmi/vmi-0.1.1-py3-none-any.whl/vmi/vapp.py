from PySide2.QtWidgets import QApplication, QStyleFactory
from PySide2.QtWinExtras import QWinTaskbarButton
import threading
import time

app = QApplication()
app.setOrganizationName('vmi')
app.setStyle(QStyleFactory.create('Fusion'))

_AppWindow = None
_TaskbarButton = QWinTaskbarButton()
_Progress = _TaskbarButton.progress()


def setAppWindow(w):
    _TaskbarButton.setParent(w)
    _TaskbarButton.setWindow(w.windowHandle())

    _Progress.setVisible(True)
    _Progress.setRange(0, 100)
    _Progress.setValue(0)


def waitThread(thread: threading.Thread, progress=None):
    while thread.isAlive():
        if progress is None:
            value = (_Progress.value() + 1) % 100
        else:
            value = progress[0]
        _Progress.setValue(value)
        time.sleep(0.1)
    _Progress.setValue(0)