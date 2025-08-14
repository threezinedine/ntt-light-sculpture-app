from typing import Any
from constants import IMAGE_PREVIEW_CHANGED_EVENT_NAME
from modules.event_system.event_system import EventSystem
from modules.history_manager import Command
from structs.project import Project


class ChangeThesholdCommand(Command):
    def __init__(self, project: Project, index: int, preValue: int):
        self._project = project
        self._index = index
        self._preValue = preValue

    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _UndoImpl(self) -> str | None:
        self._project.images[self._index].threshold = self._preValue

        EventSystem.TriggerEvent(
            IMAGE_PREVIEW_CHANGED_EVENT_NAME,
            self._index,
        )
        return None
