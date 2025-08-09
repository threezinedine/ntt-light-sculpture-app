from dataclasses import asdict
from datetime import datetime
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
from structs.project import Project
from utils.logger import logger
from utils.application import (
    GetApplicationDataFolder,
    GetApplicationDataFile,
    GetProjectDataFile,
)
from components.new_project_dialog.dialog import NewProjectDialog


@as_singleton()
@as_dependency(Application, Project)
class MainWindow(QMainWindow):
    def __init__(
        self,
        application: Application,
        project: Project,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.application = application
        self.project = project
        self._Config()

        self.ui = Ui_MainWindow()
        self.newProjectDialog = NewProjectDialog(
            self, acceptCallback=self._CreateNewProject
        )
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

        self.ui.newProjectAction.triggered.connect(self._OpenCreateNewProjectDialog)

    def _OpenCreateNewProjectDialog(self) -> None:
        self.newProjectDialog.show()

    def _CreateNewProject(self, projectDirectory: str, projectName: str) -> None:
        finalProjectDirectory = os.path.normpath(
            os.path.join(projectDirectory, projectName)
        )

        os.makedirs(finalProjectDirectory)

        projectDataFile = GetProjectDataFile(projectDirectory, projectName)
        self.project.projectName = projectName
        self.project.SetCreatedAt(datetime.now())
        self.project.SetLastEditAt(datetime.now())
        with open(projectDataFile, "w") as f:
            f.write(json.dumps(asdict(self.project)))

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(a0)  # type: ignore
