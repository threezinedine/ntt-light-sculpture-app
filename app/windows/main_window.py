from dataclasses import asdict
import os
import json
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from constants import APP_DATA_KEY
from converted_uis.main_window import Ui_MainWindow
from components.openg_widget import OpenGlWidget
from modules.dependency_injection.decorators import as_dependency, as_singleton
from structs.application import Application
from utils.logger import logger
from utils.application import GetApplicationDataFolder, GetApplicationDataFile


@as_singleton()
@as_dependency(Application)
class MainWindow(QMainWindow):
    def __init__(
        self,
        application: Application,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.application = application
        self._Config()

        self.ui = Ui_MainWindow()
        self._SetupUI()

    def _Config(self) -> None:
        """
        Used for checking the system health for the whole application.
        Be called at the start of the constructor.
        """
        if not os.environ.get(APP_DATA_KEY, None):
            logger.fatal("Application data folder is not set")
            raise EnvironmentError("Application data folder is not set")

        dataFolder = GetApplicationDataFolder()
        if not os.path.exists(dataFolder):
            try:
                os.makedirs(dataFolder)
                logger.info(f"Application data folder created: {dataFolder}")
            except Exception as e:
                logger.fatal(f"Failed to create application data folder: {e}")
                raise EnvironmentError(f"Failed to create application data folder: {e}")

        applicationJsonFile = GetApplicationDataFile()
        if not os.path.exists(applicationJsonFile):
            with open(applicationJsonFile, "w") as f:
                f.write(json.dumps(asdict(self.application)))
                logger.info(f"Application data file created: {applicationJsonFile}")

    def _SetupUI(self) -> None:
        """
        Called at the end of the constructor for managing the UI.
        """

        self.ui.setupUi(self)  # type: ignore

        self.ui.centerLayout.addWidget(OpenGlWidget())

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(a0)  # type: ignore
