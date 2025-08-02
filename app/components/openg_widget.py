from typing import Optional
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtOpenGL import QGLWidget
from Engine import Renderer


class OpenGlWidget(QGLWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super(OpenGlWidget, self).__init__(parent, shareWidget=None, flags=flags)
        self._renderer = Renderer()

    def initializeGL(self):
        self._renderer.Initialize()

    def paintGL(self):
        self._renderer.BeforeRender()
        self._renderer.Render()
        self._renderer.AfterRender()
