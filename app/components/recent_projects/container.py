from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from converted_uis.recent_projects_container import Ui_RecentProjectsContainer
from modules.dependency_injection.decorators import as_singleton


@as_singleton()
class RecentProjectsContainer(QWidget):
    def __init__(
        self,
        parent: Optional["QWidget"] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)
        self.ui = Ui_RecentProjectsContainer()
        self.ui.setupUi(self)  # type: ignore
