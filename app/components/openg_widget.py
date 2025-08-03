from typing import Optional
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Engine import Renderer


class OpenGlWidget(QOpenGLWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super(OpenGlWidget, self).__init__(parent, flags=flags)
        self._renderer = Renderer()

    def initializeGL(self):
        super(OpenGlWidget, self).initializeGL()
        try:
            self._renderer.Initialize()
        except Exception as e:
            print(e)

    def resizeGL(self, width: int, height: int):
        self._renderer.Resize(width, height)

    def paintGL(self):
        try:
            self._renderer.Render()
        except Exception as e:
            print(e)

    def closeEvent(self, event: QCloseEvent):
        self._renderer.Shutdown()
        event.accept()
