import os
from datetime import datetime
from typing import Generator, Self
from PyQt6.QtWidgets import QFileDialog
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot

from modules.dependency_injection import DependencyContainer
from structs.application import Application
from structs.project import Project
from windows.main_window import MainWindow
from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER, TEST_NEW_PROJECT_PATH
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetProjectDataFile,
    GetProjectDataFolder,
)


class FolderDialogSetup:
    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._monkeypatch = monkeypatch

    def SetOutput(self, output: str | None) -> None:
        self._monkeypatch.setattr(
            QFileDialog,
            "getExistingDirectory",
            lambda *args, **kwargs: output,  # type: ignore
        )


@pytest.fixture()
def folderDialogSetup(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[FolderDialogSetup, None, None]:
    yield FolderDialogSetup(monkeypatch)


class FileDialogSetup:
    def __init__(self, monkeypatch: pytest.MonkeyPatch) -> None:
        self._monkeypatch = monkeypatch

    def SetOutput(self, output: str | None, success: bool = True) -> None:
        self._monkeypatch.setattr(
            QFileDialog,
            "getOpenFileName",
            lambda *args, **kwargs: (output, success),  # type: ignore
        )


@pytest.fixture()
def fileDialogSetup(
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[FileDialogSetup, None, None]:
    yield FileDialogSetup(monkeypatch)


class MainWindowBuilder:
    def __init__(
        self,
        fs: FakeFilesystem,
        qtbot: QtBot,
    ) -> None:
        self._fs = fs
        self._qtbot = qtbot

    def Build(self) -> MainWindow:
        from windows.main_window import MainWindow

        mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
        self._qtbot.addWidget(mainWindow)
        mainWindow.showMaximized()

        return mainWindow


@pytest.fixture()
def mainWindowBuilder(
    fs: FakeFilesystem,
    qtbot: QtBot,
) -> Generator[MainWindowBuilder, None, None]:
    yield MainWindowBuilder(fs, qtbot)


class ProjectBuilder:
    def __init__(
        self,
        fs: FakeFilesystem,
        qtBot: QtBot,
    ) -> None:
        self._fs = fs
        self._qtBot = qtBot

        self.projectDirectory = ""
        self.projectName = ""

    def SetProjectDirectory(self, projectDirectory: str) -> Self:
        self._projectDirectory = projectDirectory
        return self

    def SetProjectName(self, projectName: str) -> Self:
        self._projectName = projectName
        return self

    def Build(self) -> Project:
        project = Project()
        project.projectName = self._projectName
        project.SetCreatedAt(datetime.now())
        project.SetLastEditAt(datetime.now())
        return project


class ApplicationBuilder:
    def __init__(
        self,
        fs: FakeFilesystem,
        qtBot: QtBot,
    ) -> None:
        self._fs = fs
        self._qtBot = qtBot

        self.appDataFolder = ""

    def RemoveAppDataFolderVariable(self) -> Self:
        os.environ.pop(APP_DATA_KEY)
        return self

    def CreateAppDataFolder(self) -> Self:
        assert os.environ.get(APP_DATA_KEY) is not None
        os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
        self._fs.create_dir(GetApplicationDataFolder())  # type: ignore
        return self

    def CreateAppDataFile(self) -> Self:
        assert self._fs.exists(GetApplicationDataFolder())  # type: ignore

        with open(GetApplicationDataFile(), "w") as f:
            f.write(Application().ToJson())

        return self


class FixtureBuilder:
    def __init__(
        self,
        fs: FakeFilesystem,
        qtBot: QtBot,
    ) -> None:
        self._fs = fs
        self._qtBot = qtBot

        self._fs.reset()
        if os.environ.get(APP_DATA_KEY) is not None:
            os.environ.pop(APP_DATA_KEY)

        self._appDataShouldBeError = False
        self._application: Application | None = None
        self._recentProjects: list[str] = []
        self._projects: dict[str, Project] = {}

    def UseAppDataApplication(self) -> Self:
        os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
        return self

    def AddAppDataFolder(self) -> Self:
        assert (
            os.environ.get(APP_DATA_KEY) is not None
        ), "AppData folder must be created first"
        assert not self._fs.exists(GetApplicationDataFolder()), "AppData folder already exists"  # type: ignore
        self._appdataDirectory = GetApplicationDataFolder()
        self._fs.create_dir(self._appdataDirectory)  # type: ignore
        return self

    def AddAppDataFile(self) -> Self:
        assert self._fs.exists(GetApplicationDataFolder()), "AppData folder must be created first"  # type: ignore
        self._application = Application()
        return self

    def AddErrorAppDataFile(self) -> Self:
        self._appDataShouldBeError = True
        return self

    def AddRecentProject(self, projectName: str) -> Self:
        assert projectName in self._projects, f"Project {projectName} does not exist"

        self._recentProjects.append(projectName)

        return self

    def AddProject(self, projectName: str) -> Self:
        assert (
            projectName not in self._projects
        ), f"Project {projectName} already exists"

        project = Project()
        project.projectName = projectName
        project.SetCreatedAt(datetime.now())
        project.SetLastEditAt(datetime.now())
        self._projects[projectName] = project

        return self

    def Build(self) -> MainWindow:
        # ================ PROJECTS CONFIGURE ===========================
        for project in self._projects.values():
            projectFolder = GetProjectDataFolder(
                TEST_NEW_PROJECT_PATH,
                project.projectName,
            )
            projectFile = GetProjectDataFile(
                TEST_NEW_PROJECT_PATH,
                project.projectName,
            )
            assert not self._fs.exists(projectFolder), f"Project folder {projectFolder} already exists"  # type: ignore
            assert not self._fs.exists(projectFile), f"Project file {projectFile} already exists"  # type: ignore

            self._fs.create_dir(projectFolder)  # type: ignore

            with open(projectFile, "w") as f:
                f.write(project.ToJson())
        # ===============================================================

        # ================ APP DATA FOLDER CONFIGURE ====================
        if self._appDataShouldBeError:
            with open(GetApplicationDataFile(), "w") as f:
                f.write('"Error": ')
        else:
            if self._application is not None:
                for projectName in self._recentProjects:
                    project = self._projects[projectName]
                    projectFolder = GetProjectDataFolder(
                        TEST_NEW_PROJECT_PATH,
                        project.projectName,
                    )
                    projectFile = GetProjectDataFile(
                        TEST_NEW_PROJECT_PATH,
                        project.projectName,
                    )
                    assert self._fs.exists(projectFolder), f"Project folder {projectFolder} does not exist"  # type: ignore
                    assert self._fs.exists(projectFile), f"Project file {projectFile} does not exist"  # type: ignore
                    self._application.recentProjectFilePaths[project.projectName] = (
                        projectFile
                    )
                    self._application.recentProjectNames.append(project.projectName)

                with open(GetApplicationDataFile(), "w") as f:
                    f.write(self._application.ToJson())
        # ===============================================================

        # ================ MAIN WINDOW CONFIGURE =========================
        mainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
        self._qtBot.addWidget(mainWindow)
        mainWindow.showMaximized()
        return mainWindow
        # ===============================================================


@pytest.fixture()
def fixtureBuilder(
    fs: FakeFilesystem,
    qtbot: QtBot,
) -> Generator[FixtureBuilder, None, None]:
    yield FixtureBuilder(fs, qtbot)
