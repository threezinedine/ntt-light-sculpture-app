from typing import Optional
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Engine import Camera, Renderer, Vec3
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

        self._moving = False

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

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        self._moving = True
        logger.debug(f"Mouse pressed at: {a0.position()}")
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._moving:
            Camera.Move(Vec3(a0.position().x(), a0.position().y(), 0), 0)
            logger.debug(f"Mouse moved to: {a0.position()}")

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self._moving = False
        return super().mouseReleaseEvent(a0)
