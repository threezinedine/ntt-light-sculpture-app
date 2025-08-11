from typing import Generator, Self
from PyQt6.QtCore import QAbstractItemModel, Qt
from PyQt6.QtWidgets import QMenu
import pytest
from pytestqt.qtbot import QtBot

from components.customs.tree_view.tree_view import CustomTreeView


class ProjectTreeActor:
    def __init__(
        self,
        qtbot: QtBot,
    ) -> None:
        self.qtbot = qtbot
        self.projectTreeView: CustomTreeView | None = None

        self._model: QAbstractItemModel | None = None
        self._contextMenu: QMenu | None = None

    def SetProjectTreeView(self, projectTreeView: CustomTreeView) -> Self:
        self.projectTreeView = projectTreeView
        self._model = self.projectTreeView.model()
        return self

    @property
    def NumberOfRows(self) -> int:
        assert self.projectTreeView is not None
        assert self._model is not None
        self._model = self.projectTreeView.model()
        return self._model.rowCount()

    def GetItemNameAt(self, index: int) -> str:
        assert self.projectTreeView is not None
        assert self._model is not None
        return self._model.index(index, 0).data(Qt.ItemDataRole.DisplayRole)

    def OpenContextMenuAt(self, index: int) -> Self:
        assert self.projectTreeView is not None
        assert self._model is not None

        item = self._model.index(index, 0)
        itemRect = self.projectTreeView.visualRect(item)
        self.qtbot.mouseClick(  # type: ignore
            self.projectTreeView.viewport(),
            Qt.MouseButton.RightButton,
            pos=itemRect.center(),
        )

        self.qtbot.wait(100)

        self._contextMenu = self.projectTreeView.findChild(QMenu)  # type: ignore
        assert self._contextMenu is not None

        return self

    def _ChooseContextMenuAction(self, actionName: str) -> None:
        assert self.projectTreeView is not None
        assert self._contextMenu is not None, "Context menu is not open"
        actions = self._contextMenu.actions()
        action = next((a for a in actions if a.text() == actionName), None)
        assert action is not None
        action.trigger()

    def ChooseDeleteAction(self) -> Self:
        self._ChooseContextMenuAction("Delete")
        return self

    def ChooseOpenImageTabAction(self) -> Self:
        self._ChooseContextMenuAction("Open")
        return self


@pytest.fixture()
def projectTreeActor(
    qtbot: QtBot,
) -> Generator[ProjectTreeActor, None, None]:
    yield ProjectTreeActor(qtbot)
