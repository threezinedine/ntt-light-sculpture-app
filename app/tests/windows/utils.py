from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from pytestqt.qtbot import QtBot
from components.customs.tree_view.tree_view import CustomTreeView


def deleteProjectTreeItem(
    qtbot: QtBot,
    projectTreeView: CustomTreeView,
    index: int,
    actionName: str,
) -> None:
    imageItem = projectTreeView.model().index(index, 0)
    imageItemRect = projectTreeView.visualRect(imageItem)
    qtbot.mouseClick(  # type: ignore
        projectTreeView.viewport(),
        Qt.MouseButton.RightButton,
        pos=imageItemRect.center(),
    )

    qtbot.wait(100)

    contextMenu: QMenu | None = projectTreeView.findChild(QMenu)  # type: ignore

    # ================== assert context menu is shown ==================
    assert contextMenu is not None
    actions = contextMenu.actions()
    action = next((a for a in actions if a.text() == actionName), None)
    assert action is not None
    action.trigger()
