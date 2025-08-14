from typing import Any
from constants import OPENGL_SETTING_CHANGED_EVENT_NAME
from modules.history_manager import Command
from structs.project import Project


class ChangeDrawEdgesCommand(Command):
    def __init__(self, project: Project, newState: bool) -> None:
        super().__init__()

        self.project = project
        self.newState = newState

    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        self.project.openglSetting.drawEdges = self.newState

    def _UndoImpl(self) -> str | None:
        self.project.openglSetting.drawEdges = not self.newState
        return OPENGL_SETTING_CHANGED_EVENT_NAME


class ChangeDrawFacesCommand(Command):
    def __init__(self, project: Project, newState: bool) -> None:
        super().__init__()

        self.project = project
        self.newState = newState

    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        self.project.openglSetting.drawFaces = self.newState

    def _UndoImpl(self) -> str | None:
        self.project.openglSetting.drawFaces = not self.newState
        return OPENGL_SETTING_CHANGED_EVENT_NAME
