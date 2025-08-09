from pyfakefs.fake_filesystem import FakeFilesystem
from datetime import datetime
import pytest  # type: ignore
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_PATH,
    TEST_PROJECT_FILE_ERROR_FOLDER,
    TEST_PROJECT_FILE_ERROR_PROJECT_NAME,
)
from tests.windows.helper import AppDataSetup, FileDialogSetup
from modules.dependency_injection import DependencyContainer
from utils.application import GetProjectDataFile, GetProjectDataFolder, GetWindowTitle


def test_open_project(
    fs: FakeFilesystem,
    qtbot: QtBot,
    appDataSetup: AppDataSetup,
    fileDialogSetup: FileDialogSetup,
    mocker: MockerFixture,
):
    from windows.main_window import MainWindow
    from structs.application import Application
    from structs.project import Project

    appDataSetup.SetupApplicationData(Application())

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    # ================================= SYSTEM HEALTH CHECK =================================
    assert mainWindow.windowTitle() == GetWindowTitle()

    # ================================= Open Errored Project =================================
    fs.create_dir(  # type: ignore
        GetProjectDataFolder(
            TEST_PROJECT_FILE_ERROR_FOLDER,
            TEST_PROJECT_FILE_ERROR_PROJECT_NAME,
        )
    )

    projectFile = GetProjectDataFile(
        TEST_PROJECT_FILE_ERROR_FOLDER,
        TEST_PROJECT_FILE_ERROR_PROJECT_NAME,
    )
    dialogMock = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")

    with open(projectFile, "w") as f:
        f.write('{"Error"}')

    fileDialogSetup.SetOutput(projectFile)
    mainWindow.ui.openProjectAction.trigger()

    assert dialogMock.call_count == 1
    assert mainWindow.windowTitle() == GetWindowTitle()

    # ================================= Open Valid Project =================================
    fs.create_dir(  # type: ignore
        GetProjectDataFolder(
            TEST_NEW_PROJECT_PATH,
            TEST_NEW_PROJECT_NAME,
        )
    )

    projectFile = GetProjectDataFile(
        TEST_NEW_PROJECT_PATH,
        TEST_NEW_PROJECT_NAME,
    )

    with open(projectFile, "w") as f:
        project = Project()
        project.projectName = TEST_NEW_PROJECT_NAME
        project.SetCreatedAt(datetime.now())
        project.SetLastEditAt(datetime.now())
        f.write(project.ToJson())

    fileDialogSetup.SetOutput(projectFile)
    mainWindow.ui.openProjectAction.trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)
