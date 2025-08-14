from typing import Any
from constants import EMPTY_HISTORY_EVENT_NAME, HISTORY_NOT_EMPTY_EVENT_NAME
import pytest  # type: ignore
from pytest_mock import MockerFixture
from modules.history_manager import Command, HistoryManager


class Global:
    count = 0


class AddOne(Command):
    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        Global.count += 1

    def _UndoImpl(self) -> None:
        Global.count -= 1


class AddTwo(Command):
    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        Global.count += 2

    def _UndoImpl(self) -> None:
        Global.count -= 2


def test_HistoryManager_Undo_EmptyHistory() -> None:
    HistoryManager.Undo()
    assert HistoryManager.IsEmpty()


def test_HistoryManager_Undo_NonEmptyHistory() -> None:
    Global.count = 0
    HistoryManager.Execute(AddOne())
    assert Global.count == 1
    HistoryManager.Undo()
    assert Global.count == 0
    assert HistoryManager.IsEmpty()


def test_HistoryManager_TriggerNotEmptyEvent(mocker: MockerFixture) -> None:
    Global.count = 0
    eventTrigger = mocker.patch(
        "modules.event_system.event_system.EventSystem.TriggerEvent"
    )

    Global.count = 0

    HistoryManager.Execute(AddOne())
    assert not HistoryManager.IsEmpty()

    eventTrigger.assert_called_once_with(HISTORY_NOT_EMPTY_EVENT_NAME)


def test_HistoryManager_TriggerEmptyEventByReset(mocker: MockerFixture) -> None:
    Global.count = 0
    HistoryManager.Execute(AddOne())

    eventTrigger = mocker.patch(
        "modules.event_system.event_system.EventSystem.TriggerEvent"
    )

    HistoryManager.Reset()
    eventTrigger.assert_called_once_with(EMPTY_HISTORY_EVENT_NAME)


def test_HistoryManager_TriggerEmptyEventByUndo(mocker: MockerFixture) -> None:
    Global.count = 0
    HistoryManager.Execute(AddOne())

    eventTrigger = mocker.patch(
        "modules.event_system.event_system.EventSystem.TriggerEvent"
    )

    HistoryManager.Undo()
    eventTrigger.assert_called_once_with(EMPTY_HISTORY_EVENT_NAME)


def test_Add_Different_Type_Of_command() -> None:
    Global.count = 0

    HistoryManager.Execute(AddTwo())
    HistoryManager.Execute(AddOne())
    HistoryManager.Execute(AddTwo())

    assert Global.count == 5
    HistoryManager.Undo()
    assert Global.count == 3
    assert not HistoryManager.IsEmpty()
    HistoryManager.Undo()
    assert Global.count == 2
    HistoryManager.Undo()
    assert Global.count == 0
    assert HistoryManager.IsEmpty()
