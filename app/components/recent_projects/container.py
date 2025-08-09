from typing import Optional
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt
from constants import (
    APPLICATION_LOADED_EVENT_NAME,
    APPLICATION_UPDATED_EVENT_NAME,
)
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

        self.hasNoRecentProjectsLabel: QLabel | None = None

        self._setupUI()

    def _setupUI(self) -> None:
        logger.debug(self.application.recentProjectFilePaths)
        hasNoRecentProjectsLabels = self.findChildren(QLabel)  # type: ignore
        assert len(hasNoRecentProjectsLabels) == 1
        self.hasNoRecentProjectsLabel = hasNoRecentProjectsLabels[0]  # type: ignore
        self._reloadRecentProjects()
        EventSystem.RegisterEvent(
            APPLICATION_LOADED_EVENT_NAME,
            self._reloadRecentProjects,
        )
        EventSystem.RegisterEvent(
            APPLICATION_UPDATED_EVENT_NAME,
            self._removeRecentProject,
        )

    def _removeRecentProject(self) -> None:
        if len(self.application.recentProjectFilePaths.keys()) == 0:
            if self.hasNoRecentProjectsLabel is not None:
                self.ui.RecentsProjectLayout.addWidget(self.hasNoRecentProjectsLabel)
                self.hasNoRecentProjectsLabel.show()

        recentProjectsItems: list[RecentProjectsItem] = self.findChildren(RecentProjectsItem)  # type: ignore
        for recentProjectsItem in recentProjectsItems:
            if (
                recentProjectsItem.projectName
                not in self.application.recentProjectFilePaths.keys()
            ):
                recentProjectsItem.setParent(None)  # type: ignore
                break

    def _reloadRecentProjects(self) -> None:
        if len(self.application.recentProjectFilePaths.keys()) != 0:
            self.hasNoRecentProjectsLabel.setParent(None)  # type: ignore

        for (
            projectName,
            projectFilePath,
        ) in self.application.recentProjectFilePaths.items():
            recentProjectsItem = RecentProjectsItem(projectName, projectFilePath)
            self.ui.RecentsProjectLayout.addWidget(recentProjectsItem)
