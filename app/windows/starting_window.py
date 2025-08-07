from dataclasses import asdict
import os
import json
from utils.logger import logger
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from components.recent_projects.container import RecentProjectsContainer
from constants import APP_DATA_KEY, APPLICATION_DATA_FILE, APPLICATION_DATA_FOLDER
from converted_uis.starting_window import Ui_StartingWindow
from modules.dependency_injection import DependencyContainer
from modules.dependency_injection.decorators import as_singleton, as_dependency
from structs.application import Application


@as_singleton()
@as_dependency(Application)
class StartingWindow(QMainWindow):
    def __init__(
        self,
        application: Application,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        if APP_DATA_KEY not in os.environ:
            message = f'The environment variable "{APP_DATA_KEY}" is not set'
            logger.fatal(message)
            raise EnvironmentError(message)

        applicationAppDataFolder = os.path.join(
            os.environ[APP_DATA_KEY], APPLICATION_DATA_FOLDER
        )
        if not os.path.exists(applicationAppDataFolder):
            logger.info(
                f'Folder "{applicationAppDataFolder}" does not exist. Creating it...'
            )
            os.makedirs(applicationAppDataFolder)

        applicationFile = os.path.join(applicationAppDataFolder, APPLICATION_DATA_FILE)
        if not os.path.exists(applicationFile):
            logger.info(f'File "{applicationFile}" does not exist. Creating it...')
            with open(applicationFile, "w") as f:
                f.write(json.dumps(asdict(application), indent=4))

        self.application = application

        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)  # type: ignore

        self._setupUI()

    def _setupUI(self) -> None:
        self.setFixedSize(self.size())
        self.setWindowTitle(f"Light Sculpture Studio - v{self.application.version}")

        self.ui.RecentProjectsLayout.addWidget(
            DependencyContainer.GetInstance(
                RecentProjectsContainer.__name__,
            )
        )
