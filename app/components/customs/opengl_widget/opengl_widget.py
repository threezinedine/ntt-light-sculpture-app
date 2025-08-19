from datetime import datetime
from typing import Optional
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent, QMouseEvent
from PyQt6.QtWidgets import QWidget
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from Engine import Camera, Position, Renderer, Vec3
from modules.dependency_injection import DependencyContainer
from modules.history_manager import HistoryManager
from structs.project import Project
from utils.logger import logger
from .commands import ChangeOriginCommand


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
        self._startTime: datetime = datetime.now()
        self._prevMousePosition: Position | None = None

        self._project: Project = DependencyContainer.GetInstance(Project.__name__)

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
        self._startTime = datetime.now()
        self._prevMousePosition = Position(a0.position().x(), a0.position().y(), 0)
        return super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self._moving:
            assert (
                self._prevMousePosition is not None
            ), "Previous mouse position must be set before moving"

            currentTime = datetime.now()
            elapsed = currentTime - self._startTime
            currentPosition = Position(a0.position().x(), a0.position().y(), 0)
            Camera.Move(
                Vec3(
                    currentPosition.x() - self._prevMousePosition.x(),
                    currentPosition.y() - self._prevMousePosition.y(),
                    0,
                ),
                elapsed.total_seconds(),
            )
            self._prevMousePosition = currentPosition
            self._startTime = currentTime

        return super().mouseMoveEvent(a0)

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
        self._moving = False
        HistoryManager.Execute(
            ChangeOriginCommand(self._project.openglSetting, Camera.GetOrigin())
        )
        return super().mouseReleaseEvent(a0)
