from abc import ABC, abstractmethod
from typing import Any

from constants import (
    COMMAND_CAN_NOT_BE_EXECUTED_EVENT_NAME,
    EMPTY_HISTORY_EVENT_NAME,
    HISTORY_NOT_EMPTY_EVENT_NAME,
)
from modules.event_system.event_system import EventSystem


class Command(ABC):
    """
    All actions inside the project which can affect the data storage should be implemented
        as the subclasses of this Command class which help that action can be restored. Some
        specific actions like adjusting the slider can record the start and end values.
    """

    def Execute(self, *args: Any, **kwargs: Any) -> None:
        self._ExecuteImpl(*args, **kwargs)

    @abstractmethod
    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError("Subclasses must implement _ExecuteImpl method.")

    def Undo(self) -> None:
        self._UndoImpl()

    @abstractmethod
    def _UndoImpl(self) -> None:
        raise NotImplementedError("Subclasses must implement _UndoImpl method.")

    def CanBeExecuted(self) -> bool:
        """
        This method can be overridden to provide custom execution logic.
        """
        return True


class HistoryManager:
    """
    Be used as static hub for all incoming actions.
    """

    _history: list[Command] = []

    @staticmethod
    def IsEmpty() -> bool:
        return len(HistoryManager._history) == 0

    @staticmethod
    def Reset() -> None:
        """
        Delete all commands, from now on, cannot be undone.
        """
        HistoryManager._history.clear()
        EventSystem.TriggerEvent(EMPTY_HISTORY_EVENT_NAME)

    @staticmethod
    def Undo() -> None:
        """
        If has no commands, do nothing, if the, the history is empty after this call, trigger the empty history event.
        """

        if HistoryManager.IsEmpty():
            return

        last_command = HistoryManager._history.pop()
        last_command.Undo()

        if HistoryManager.IsEmpty():
            EventSystem.TriggerEvent(EMPTY_HISTORY_EVENT_NAME)

    @staticmethod
    def Execute(command: Command) -> None:
        """
        Automatically execute the command if it's executed.
        If cannot be executed, an event is trigger.

        If the current history is empty, the executed command trigger an event.
        """
        if not command.CanBeExecuted():
            EventSystem.TriggerEvent(COMMAND_CAN_NOT_BE_EXECUTED_EVENT_NAME)
            return

        command.Execute()
        HistoryManager._history.append(command)
        if len(HistoryManager._history) == 1:
            EventSystem.TriggerEvent(HISTORY_NOT_EMPTY_EVENT_NAME)
