import os
from datetime import datetime
from typing import Generator, Any
from PyQt6.QtWidgets import QFileDialog
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot

from modules.dependency_injection import DependencyContainer
from windows.main_window import MainWindow
from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetProjectDataFile,
    GetProjectDataFolder,
)


class AppDataSetup:
    def SetupApplicationData(self, application: Any) -> None:
        with open(GetApplicationDataFile(), "w") as f:
            f.write(application.ToJson())


@pytest.fixture()
def appDataSetup(fs: FakeFilesystem) -> Generator[AppDataSetup, None, None]:
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    fs.create_dir(GetApplicationDataFolder())  # type: ignore

    yield AppDataSetup()


class ProjectSetup:
    def __init__(self, fs: FakeFilesystem) -> None:
        self._fs = fs

    def SetupProjectData(self, projectDirectory: str, projectName: str) -> None:
        from structs.project import Project

        project = Project()
        project.projectName = projectName
        project.SetCreatedAt(datetime.now())
        project.SetLastEditAt(datetime.now())

        self._fs.create_dir(GetProjectDataFolder(projectDirectory, projectName))  # type: ignore

        with open(GetProjectDataFile(projectDirectory, projectName), "w") as f:
            f.write(project.ToJson())


@pytest.fixture()
def projectSetup(fs: FakeFilesystem) -> Generator[ProjectSetup, None, None]:
    yield ProjectSetup(fs)


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

    def SetOutput(self, output: str | None) -> None:
        self._monkeypatch.setattr(
            QFileDialog,
            "getOpenFileName",
            lambda *args, **kwargs: output,  # type: ignore
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
        appDataSetup: AppDataSetup,
    ) -> None:
        self._fs = fs
        self._qtbot = qtbot
        self._appDataSetup = appDataSetup

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
    appDataSetup: AppDataSetup,
) -> Generator[MainWindowBuilder, None, None]:
    yield MainWindowBuilder(fs, qtbot, appDataSetup)
