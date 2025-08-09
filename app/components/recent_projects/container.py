from typing import Optional
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from constants import APPLICATION_LOADED_EVENT_NAME
from converted_uis.recent_projects_container import Ui_RecentProjectsContainer
from modules.dependency_injection.decorators import as_dependency, as_singleton
from modules.event_system.event_system import EventSystem
from structs.application import Application
from utils.logger import logger
from .item import RecentProjectsItem


@as_singleton()
@as_dependency(Application)
class RecentProjectsContainer(QWidget):
    def __init__(
        self,
        application: Application,
        parent: Optional["QWidget"] = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.application = application

        self.ui = Ui_RecentProjectsContainer()
        self.ui.setupUi(self)  # type: ignore

        self._setupUI()

    def _setupUI(self) -> None:
        logger.debug(self.application.recentProjectFilePaths)
        self._reloadRecentProjects()
        EventSystem.RegisterEvent(
            APPLICATION_LOADED_EVENT_NAME,
            self._reloadRecentProjects,
        )

    def _reloadRecentProjects(self) -> None:
        hasNoRecentProjectsLabel = self.findChildren(QLabel)  # type: ignore
        assert len(hasNoRecentProjectsLabel) == 1
        logger.debug(f"hasNoRecentProjectsLabel: {hasNoRecentProjectsLabel}")

        if len(self.application.recentProjectFilePaths.keys()) != 0:
            for child in hasNoRecentProjectsLabel:
                child.setParent(None)  # type: ignore

        for (
            projectName,
            projectFilePath,
        ) in self.application.recentProjectFilePaths.items():
            logger.debug(f"Adding recent project: {projectName} - {projectFilePath}")
            recentProjectsItem = RecentProjectsItem(projectName, projectFilePath)
            self.ui.RecentsProjectLayout.addWidget(recentProjectsItem)
