import os
from datetime import datetime
import shutil
from typing import Generator, Self
from PyQt6.QtWidgets import QFileDialog
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot

from modules.dependency_injection import DependencyContainer
from structs.application import Application
from structs.image_meta import ImageMeta
from structs.project import Project
from windows.main_window import MainWindow
from constants import (
    APP_DATA_KEY,
    TEST_APP_DATA_FOLDER,
    TEST_NEW_PROJECT_PATH,
)
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetImageFileNameFromFilePath,
    GetImageFilePath,
    GetImageFolder,
    GetImageMetadataFile,
    GetProjectDataFile,
    GetProjectDataFolder,
    GetTestProjectDataFolder,
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
    ) -> None:
        self._project = Project()
        self._useErrorProjectFile = False
        self._createProjectFile = True
        self._imagePaths: list[str] = []

    def Name(self, projectName: str) -> Self:
        self._project.projectName = projectName
        return self

    def NotCreateProjectFile(self) -> Self:
        self._createProjectFile = False
        return self

    def UseErrorProjectFile(self) -> Self:
        self._useErrorProjectFile = True
        return self

    def AddImage(self, imagePath: str) -> Self:
        self._imagePaths.append(imagePath)
        return self

    def Build(self, fs: FakeFilesystem) -> None:
        projectFolder = GetProjectDataFolder(
            TEST_NEW_PROJECT_PATH,
            self._project.projectName,
        )
        assert not fs.exists(projectFolder), f"Project folder {projectFolder} already exists"  # type: ignore
        fs.create_dir(projectFolder)  # type: ignore

        for imagePath in self._imagePaths:
            imageName = GetImageFileNameFromFilePath(imagePath)
            imageFolder = GetImageFolder(
                GetTestProjectDataFolder(self._project.projectName)
            )

            if not os.path.exists(imageFolder):
                os.makedirs(imageFolder)

            finalImagePath = GetImageFilePath(
                GetTestProjectDataFolder(self._project.projectName),
                imageName,
            )

            assert not fs.exists(finalImagePath), f"Image file {finalImagePath} already exists"  # type: ignore
            fs.add_real_file(imagePath, read_only=True)  # type: ignore
            assert fs.exists(imagePath), f"Image file {imagePath} does not exist"  # type: ignore

            self._project.images.append(imageName)
            shutil.copyfile(
                imagePath,
                GetImageFilePath(
                    GetTestProjectDataFolder(self._project.projectName), imageName
                ),
            )

            with open(
                GetImageMetadataFile(
                    GetTestProjectDataFolder(self._project.projectName), imageName
                ),
                "w",
            ) as f:
                f.write(ImageMeta().ToJson())

        self._project.SetCreatedAt(datetime.now())
        self._project.SetLastEditAt(datetime.now())

        projectFile = GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            self._project.projectName,
        )
        assert not fs.exists(projectFile), f"Project file {projectFile} already exists"  # type: ignore

        if not self._createProjectFile:
            return

        if self._useErrorProjectFile:
            with open(projectFile, "w") as f:
                f.write('"Error": ')
            return

        with open(projectFile, "w") as f:
            f.write(self._project.ToJson())


class ApplicationBuilder:
    def __init__(
        self,
    ) -> None:
        os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER

        self._appDataFileShouldBeError = False
        self._createAppDataFolder = True
        self._createAppDataFile = True
        self._saveErrorAppDataFile = False
        self._application: Application = Application()

    def NotUseAppDataEnvironmentVariable(self) -> Self:
        if APP_DATA_KEY in os.environ:
            os.environ.pop(APP_DATA_KEY)
        return self

    def DontAddAppDataFolder(self) -> Self:
        self._createAppDataFolder = False
        self._createAppDataFile = False
        return self

    def AddErrorAppDataFile(self) -> Self:
        assert self._createAppDataFolder, "AppData folder must be created first"
        self._appDataFileShouldBeError = True
        return self

    def DontAddAppDataFile(self) -> Self:
        self._createAppDataFile = False
        return self

    def Version(self, major: int, minor: int, patch: int) -> Self:
        assert self._application is not None, "Application must be created first"
        self._application.version.major = major
        self._application.version.minor = minor
        self._application.version.patch = patch
        return self

    def AddRecentProject(self, projectName: str) -> Self:
        projectFile = GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            projectName,
        )
        self._application.recentProjectNames.append(projectName)
        self._application.recentProjectFilePaths[projectName] = projectFile
        return self

    def AddErrorRecentProject(self, projectName: str, projectFilePath: str) -> Self:
        self._application.recentProjectNames.append(projectName)
        self._application.recentProjectFilePaths[projectName] = projectFilePath
        return self

    def Build(self, fs: FakeFilesystem) -> None:
        if os.environ.get(APP_DATA_KEY) is None:
            return

        assert not fs.exists(GetApplicationDataFolder()), "AppData folder already exists"  # type: ignore

        if not self._createAppDataFolder:
            assert (
                not self._appDataFileShouldBeError
            ), "AppData file should be error settup wrong"
            return

        fs.create_dir(GetApplicationDataFolder())  # type: ignore

        if self._appDataFileShouldBeError:
            assert self._createAppDataFile, "AppData file should be error settup wrong"
            with open(GetApplicationDataFile(), "w") as f:
                f.write('"Error": ')
            return

        assert not fs.exists(GetApplicationDataFile()), "AppData file already exists"  # type: ignore

        if not self._createAppDataFile:
            return

        with open(GetApplicationDataFile(), "w") as f:
            f.write(self._application.ToJson())


class FixtureBuilder:
    def __init__(
        self,
        fs: FakeFilesystem,
        qtBot: QtBot,
    ) -> None:
        self._fs = fs
        self._qtBot = qtBot

        self._projectBuilders: list[ProjectBuilder] = []
        self._applicationBuilder: ApplicationBuilder | None = None

    def AddApplication(self, builder: ApplicationBuilder) -> Self:
        assert self._applicationBuilder is None, "Application already exists"
        self._applicationBuilder = builder
        return self

    def AddProject(self, builder: ProjectBuilder) -> Self:
        self._projectBuilders.append(builder)
        return self

    def AddRealFile(self, filePath: str) -> Self:
        self._fs.add_real_file(filePath, read_only=True)  # type: ignore
        return self

    def Build(self) -> MainWindow:
        # ================ PROJECTS CONFIGURE ===========================
        for project in self._projectBuilders:
            project.Build(self._fs)
        # ===============================================================

        # ================ APP DATA FOLDER CONFIGURE ====================
        if self._applicationBuilder is not None:
            self._applicationBuilder.Build(self._fs)
        else:
            ApplicationBuilder().Build(self._fs)
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
