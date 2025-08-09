from typing import Optional
from PyQt6.QtWidgets import QMessageBox, QWidget
from PyQt6.QtCore import Qt
from constants import OPEN_NON_EXISTED_PROJECT_DIR_EVENT_NAME
from converted_uis.recent_project_widget import Ui_RecentProjectItem
from modules.event_system.event_system import EventSystem


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

        self.projectName = projectName
        self.projectFilePath = projectFilePath

        self._setupUI()

    def _setupUI(self) -> None:
        self.ui.ProjectNameLabel.setText(self.projectName)
        self.ui.OpenRecentProjectButton.clicked.connect(self._onClickOpenProject)

    def _onClickOpenProject(self) -> None:
        QMessageBox.information(self, "Open Project", "Open Project")
        self.setParent(None)  # type: ignore
        EventSystem.TriggerEvent(
            OPEN_NON_EXISTED_PROJECT_DIR_EVENT_NAME,
            self.projectName,
        )
