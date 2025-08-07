from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from converted_uis.recent_projects_container import Ui_RecentProjectsContainer
from modules.dependency_injection.decorators import as_dependency, as_singleton
from structs.application import Application
from utils.logger import logger


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

    def _setupUI(self) -> None:
        logger.debug(self.application.recentProjectFilePaths)
        hasNoRecentProjectsLabel = self.findChildren(QLabel)  # type: ignore
        assert len(hasNoRecentProjectsLabel) == 1

        if len(self.application.recentProjectFilePaths.keys()) != 0:
            hasNoRecentProjectsLabel.setParent(None)  # type: ignore
