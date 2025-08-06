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

    def initializeGL(self):
        try:
            Renderer.Initialize()
        except Exception as e:
            print(e)

    def resizeGL(self, w: int, h: int):
        Renderer.Resize(w, h)

    def paintGL(self):
        try:
            Renderer.Render()
        except Exception as e:
            print(e)

    def closeEvent(self, a0: QCloseEvent):
        Renderer.Shutdown()
        a0.accept()
