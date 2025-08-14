from dataclasses import asdict
import json
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
    GetImageFolder,
    GetImageMetadataFile,
    GetProjectDataFile,
    GetProjectDataFolder,
    GetProjectNameFromFilePath,
    GetWindowTitle,
)
from constants import (
    APP_DATA_KEY,
    CHANGE_PROJECT_EVENT_NAME,
    MODIFY_IMAGES_LIST_EVENT_NAME,
    MAX_NUMBER_OF_RECENT_PROJECTS,
    RECENT_PROJECTS_EVENT_NAME,
)
from Engine import Camera, Position


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

        testPosition = Position(1, 2, 3)
        otherPosition = Position(testPosition)
        print(otherPosition.x(), otherPosition.y(), otherPosition.z())
        origin = Camera.GetOrigin()
        print(origin.x(), origin.y(), origin.z())
        origin.set(1, 3, 2)
        print(origin.x(), origin.y(), origin.z())

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
                    self._UpdateApplicationDataFile()
                else:
                    # Reload recent projects
                    if len(self.application.recentProjectNames) > 0:
                        projectName = self.application.recentProjectNames[0]
                        projectFilePath = self.application.recentProjectFilePaths[
                            projectName
                        ]
                        success = self.OpenProject(projectFilePath)

                        if not success:
                            QMessageBox.information(
                                None,  # type: ignore
                                "Error",
                                f'Project "{projectName}" is invalid',
                            )
                            EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)

        # ================ Event callbacks setup ==================
        EventSystem.RegisterEvent(
            MODIFY_IMAGES_LIST_EVENT_NAME,
            self._UpdateProjectDataFile,
        )

    def CreateNewProject(self, projectDirectory: str, projectName: str) -> None:
        os.makedirs(GetProjectDataFolder(projectDirectory, projectName))

        projectDataFile = GetProjectDataFile(projectDirectory, projectName)
        self.project.projectName = projectName
        self.project.SetCreatedAt(datetime.now())
        self.project.SetLastEditAt(datetime.now())
        with open(projectDataFile, "w") as f:
            f.write(self.project.ToJson())

        imageFolder = GetImageFolder(
            GetProjectDataFolder(projectDirectory, projectName)
        )
        if not os.path.exists(imageFolder):
            os.makedirs(imageFolder)
            logger.info(f"Image folder created: {imageFolder}")

        EventSystem.TriggerEvent(CHANGE_PROJECT_EVENT_NAME)
        self.application.recentProjectFilePaths[projectName] = GetProjectDataFile(
            projectDirectory, projectName
        )
        self.application.recentProjectNames.insert(0, projectName)
        with open(GetApplicationDataFile(), "w") as f:
            f.write(self.application.ToJson())

        EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)

    def OpenProject(self, projectFile: str) -> bool:
        projectName = GetProjectNameFromFilePath(projectFile)

        if not os.path.exists(projectFile):
            localProjectName = projectName
            if not os.path.isfile(projectFile):
                for key, value in self.application.recentProjectFilePaths.items():
                    if value == projectFile:
                        localProjectName = key
                        break

            self._RemoveRecentProject(localProjectName)
            return False

        imageFolder = GetImageFolder(self.application.CurrentProjectDirectory)

        if not os.path.exists(imageFolder):
            os.makedirs(imageFolder)
            logger.info(f"Image folder created: {imageFolder}")

        with open(projectFile, "r") as f:
            valid = self.project.FromJson(f.read())
            if not valid:
                self._RemoveRecentProject(projectName)
                return False

        self._AddRecentProject(self.project.projectName, projectFile)

        EventSystem.TriggerEvent(CHANGE_PROJECT_EVENT_NAME)
        EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)
        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)
        return True

    def SaveProject(self) -> None:
        for imageMeta in self.project.images:
            imageMetaDataFile = GetImageMetadataFile(
                self.application.CurrentProjectDirectory,
                imageMeta.name,
            )

            with open(imageMetaDataFile, "w") as f:
                logger.debug(f"Saving image metadata to {imageMetaDataFile}")
                f.write(json.dumps(asdict(imageMeta), indent=4))

        self._UpdateProjectDataFile()

    def _RemoveRecentProject(self, projectName: str) -> None:
        if projectName in self.application.recentProjectNames:
            self.application.recentProjectNames.remove(projectName)
        if projectName in self.application.recentProjectFilePaths:
            del self.application.recentProjectFilePaths[projectName]

        self._UpdateApplicationDataFile()

    def _AddRecentProject(self, projectName: str, projectFilePath: str) -> None:
        if projectName in self.application.recentProjectNames:
            self.application.recentProjectNames.remove(projectName)
        if projectName in self.application.recentProjectFilePaths:
            del self.application.recentProjectFilePaths[projectName]

        self.application.recentProjectNames.insert(0, projectName)
        self.application.recentProjectFilePaths[projectName] = projectFilePath

        if len(self.application.recentProjectNames) > MAX_NUMBER_OF_RECENT_PROJECTS:
            removedProjectNames = self.application.recentProjectNames.pop()
            del self.application.recentProjectFilePaths[removedProjectNames]

        self._UpdateApplicationDataFile()

    def _UpdateProjectDataFile(self) -> None:
        currentProjectName = self.project.projectName
        currentProjectFile = self.application.recentProjectFilePaths[currentProjectName]
        with open(currentProjectFile, "w") as f:
            f.write(self.project.ToJson())

    def _UpdateApplicationDataFile(self) -> None:
        with open(GetApplicationDataFile(), "w") as f:
            f.write(self.application.ToJson())

    @property
    def WindowTitle(self) -> str:
        return GetWindowTitle(self.project.projectName)

    @property
    def RecentProjects(self) -> list[tuple[str, str]]:
        return [
            (name, self.application.recentProjectFilePaths[name])
            for name in self.application.recentProjectNames
        ]
