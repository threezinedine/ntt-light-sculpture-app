from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Engine import Application


class OpenGlWidget(QOpenGLWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super(OpenGlWidget, self).__init__(parent, flags=flags)
        self._application = Application()

    def initializeGL(self):
        try:
            self._application.Initialize()
        except Exception as e:
            print(e)

    def resizeGL(self, w: int, h: int):
        self._application.Resize(w, h)

    def paintGL(self):
        try:
            self._application.Update()
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QCloseEvent):
        self._application.Finalize()
        a0.accept()
