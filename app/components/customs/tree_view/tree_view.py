from typing import Callable
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QTreeView, QWidget


class CustomTreeView(QTreeView):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._callback: Callable[[QMouseEvent], None] | None = None
        print("CustomTreeView")

    def SetMousePressEventCallBack(
        self, callback: Callable[[QMouseEvent], None]
    ) -> None:
        self._callback = callback

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if self._callback is not None:
            self._callback(e)
        super().mousePressEvent(e)
