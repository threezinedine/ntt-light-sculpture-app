from typing import Optional
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Engine import Renderer
from utils.logger import logger


class OpenGLWidget(QOpenGLWidget):
    def __init__(
        self,
        parent: Optional[QWidget] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super(OpenGLWidget, self).__init__(parent, flags=flags)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # Approximately 60 FPS

    def initializeGL(self):
        try:
            Renderer.Initialize()
        except Exception as e:
            logger.error(e)

    def resizeGL(self, w: int, h: int):
        Renderer.Resize(w, h)

    def paintGL(self):
        try:
            Renderer.Render()
        except Exception as e:
            logger.error(e)

    def closeEvent(self, a0: QCloseEvent):
        Renderer.Shutdown()
        a0.accept()
