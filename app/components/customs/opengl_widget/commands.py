from typing import Any
from Engine import Position, Camera
from modules.history_manager import Command
from structs.opengl_setting import OpenGLSetting

from utils.logger import logger  # type: ignore


class ChangeOriginCommand(Command):
    def __init__(self, openglSetting: OpenGLSetting, newOrigin: Position):
        super().__init__()
        self._openglSetting = openglSetting
        self._newOrigin = newOrigin
        self._oldOrigin = openglSetting.origin

    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        self._openglSetting.origin = [
            self._newOrigin.x(),
            self._newOrigin.y(),
            self._newOrigin.z(),
        ]

    def _UndoImpl(self) -> str | None:
        self._openglSetting.origin = self._oldOrigin
        Camera.SetOrigin(
            Position(
                self._oldOrigin[0],
                self._oldOrigin[1],
                self._oldOrigin[2],
            )
        )
