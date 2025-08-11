from typing import Callable
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtWidgets import QTreeView, QWidget


class CustomTreeView(QTreeView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._mousePressCallback: Callable[[QMouseEvent], None] | None = None
        self._keyPressCallback: Callable[[QKeyEvent, int], None] | None = None
        print("CustomTreeView")

    def SetMousePressEventCallBack(
        self, callback: Callable[[QMouseEvent], None]
    ) -> None:
        self._mousePressCallback = callback

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self._mousePressCallback is not None:
            self._mousePressCallback(e)
        super().mousePressEvent(e)

    def SetKeyPressEventCallBack(
        self, callback: Callable[[QKeyEvent, int], None]
    ) -> None:
        self._keyPressCallback = callback

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if self._keyPressCallback is not None:
            self._keyPressCallback(event, self.currentIndex().row())
        super().keyPressEvent(event)
