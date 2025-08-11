from typing import Self
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from pytestqt.qtbot import QtBot

from components.customs.tree_view.tree_view import CustomTreeView


class ProjectTreeActor:
    def __init__(
        self,
        qtbot: QtBot,
        projectTreeView: CustomTreeView,
    ) -> None:
        self.qtbot = qtbot
        self.projectTreeView = projectTreeView

        self._model = self.projectTreeView.model()
        self._contextMenu: QMenu | None = None

    @property
    def NumberOfRows(self) -> int:
        assert self._model is not None
        self._model = self.projectTreeView.model()
        return self._model.rowCount()

    def GetItemNameAt(self, index: int) -> str:
        assert self._model is not None
        return self._model.index(index, 0).data(Qt.ItemDataRole.DisplayRole)

    def OpenContextMenuAt(self, index: int) -> Self:
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

    def DeleteImage(self) -> Self:
        assert self._contextMenu is not None, "Context menu is not open"

        actions = self._contextMenu.actions()
        action = next((a for a in actions if a.text() == "Delete"), None)
        assert action is not None
        action.trigger()
        self._contextMenu = None

        return self
