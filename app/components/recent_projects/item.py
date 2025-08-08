from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from converted_uis.recent_project_widget import Ui_RecentProjectItem


class RecentProjectsItem(QWidget):
    def __init__(
        self,
        projectName: str,
        projectFilePath: str,
        parent: Optional["QWidget"] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)
        self.ui = Ui_RecentProjectItem()
        self.ui.setupUi(self)  # type: ignore

        self.projectFilePath = projectFilePath
        self.ui.ProjectNameLabel.setText(projectName)
