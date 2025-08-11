import os
from datetime import datetime

from PyQt6.QtWidgets import QMessageBox
from components.new_project_dialog.viewmodel import NewProjectDialogViewModel
from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from structs.application import Application
from structs.project import Project

from utils.logger import logger
from utils.application import (
    GetApplicationDataFolder,
    GetApplicationDataFile,
    GetProjectDataFile,
    GetProjectDataFolder,
    GetProjectNameFromFilePath,
    GetWindowTitle,
)
from constants import (
    APP_DATA_KEY,
    CHANGE_PROJECT_EVENT_NAME,
    MAX_NUMBER_OF_RECENT_PROJECTS,
    RECENT_PROJECTS_EVENT_NAME,
)


@as_dependency(Application, Project, NewProjectDialogViewModel)
class MainWindowViewModel:
    def __init__(
        self,
        application: Application,
        project: Project,
        newProjectDialogViewModel: NewProjectDialogViewModel,
    ) -> None:
        self.application = application
        self.project = project
        self.newProjectDialogViewModel = newProjectDialogViewModel
        self.newProjectDialogViewModel.SetAcceptCallback(self.CreateNewProject)

    def Config(self) -> None:
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
                f.write(self.application.ToJson())
                logger.info(f"Application data file created: {applicationJsonFile}")
        else:
            with open(applicationJsonFile, "r") as f:
                validate = self.application.FromJson(f.read())

                if not validate:
                    logger.warning(
                        f"Application data file is invalid: {applicationJsonFile}"
                    )
                    self.application = Application()
                    with open(applicationJsonFile, "w") as f:
                        f.write(self.application.ToJson())
                else:
                    # Reload recent projects
                    if len(self.application.recentProjectNames) > 0:
                        projectFilePath = self.application.recentProjectFilePaths[
                            self.application.recentProjectNames[0]
                        ]
                        projectName = GetProjectNameFromFilePath(projectFilePath)
                        success = self.OpenProject(projectFilePath)

                        if not success:
                            QMessageBox.information(
                                None,  # type: ignore
                                "Error",
                                f'Project "{projectName}" is invalid',
                            )

    def CreateNewProject(self, projectDirectory: str, projectName: str) -> None:
        os.makedirs(GetProjectDataFolder(projectDirectory, projectName))

        projectDataFile = GetProjectDataFile(projectDirectory, projectName)
        self.project.projectName = projectName
        self.project.SetCreatedAt(datetime.now())
        self.project.SetLastEditAt(datetime.now())
        with open(projectDataFile, "w") as f:
            f.write(self.project.ToJson())

        EventSystem.TriggerEvent(CHANGE_PROJECT_EVENT_NAME)
        self.application.recentProjectFilePaths[projectName] = GetProjectDataFolder(
            projectDirectory, projectName
        )
        self.application.recentProjectNames.insert(0, projectName)
        with open(GetApplicationDataFile(), "w") as f:
            f.write(self.application.ToJson())

        EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)

    def OpenProject(self, projectFile: str) -> bool:
        if not os.path.exists(projectFile):
            projectName = GetProjectNameFromFilePath(projectFile)
            if projectName in self.application.recentProjectNames:
                self.application.recentProjectNames.remove(projectName)
            if projectName in self.application.recentProjectFilePaths:
                del self.application.recentProjectFilePaths[projectName]
            with open(GetApplicationDataFile(), "w") as f:
                f.write(self.application.ToJson())
            return False

        with open(projectFile, "r") as f:
            valid = self.project.FromJson(f.read())
            if not valid:
                projectName = GetProjectNameFromFilePath(projectFile)
                if projectName in self.application.recentProjectNames:
                    self.application.recentProjectNames.remove(projectName)
                if projectName in self.application.recentProjectFilePaths:
                    del self.application.recentProjectFilePaths[projectName]
                with open(GetApplicationDataFile(), "w") as f:
                    f.write(self.application.ToJson())

                return False

        if self.project.projectName in self.application.recentProjectNames:
            self.application.recentProjectNames.remove(self.project.projectName)

        self.application.recentProjectNames.insert(0, self.project.projectName)

        if len(self.application.recentProjectNames) > MAX_NUMBER_OF_RECENT_PROJECTS:
            removedProjectNames = self.application.recentProjectNames.pop()
            del self.application.recentProjectFilePaths[removedProjectNames]

        self.application.recentProjectFilePaths[self.project.projectName] = projectFile

        with open(GetApplicationDataFile(), "w") as f:
            f.write(self.application.ToJson())

        EventSystem.TriggerEvent(CHANGE_PROJECT_EVENT_NAME)
        EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)
        return True

    @property
    def WindowTitle(self) -> str:
        return GetWindowTitle(self.project.projectName)

    @property
    def RecentProjects(self) -> list[tuple[str, str]]:
        return [
            (name, self.application.recentProjectFilePaths[name])
            for name in self.application.recentProjectNames
        ]
