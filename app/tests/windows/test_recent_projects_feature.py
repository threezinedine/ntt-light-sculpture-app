from PyQt6.QtGui import QAction
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem

from constants import TEST_NEW_PROJECT_NAME, TEST_NEW_PROJECT_PATH
from tests.windows.helper import AppDataSetup, MainWindowBuilder, ProjectSetup
from utils.application import GetProjectDataFile, GetWindowTitle
from windows.main_window import MainWindow
from structs.application import Application


def test_recent_projects_feature(
    qtbot: QtBot,
    fs: FakeFilesystem,
    appDataSetup: AppDataSetup,
    projectSetup: ProjectSetup,
    mainWindowBuilder: MainWindowBuilder,
):
    projectSetup.SetupProjectData(TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME)

    application = Application()
    application.recentProjectFilePaths[TEST_NEW_PROJECT_NAME] = GetProjectDataFile(
        TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME
    )
    application.recentProjectNames.append(TEST_NEW_PROJECT_NAME)
    appDataSetup.SetupApplicationData(application)

    mainWindow: MainWindow = mainWindowBuilder.Build()

    noProjectAction: QAction = mainWindow.ui.noProjectsAction
    recentProjectsActions: list[QAction] = mainWindow.recentProjectsActions

    # ================================= Test No Project =================================
    assert not noProjectAction.isVisible()
    assert len(recentProjectsActions) == 1
    assert recentProjectsActions[0].isVisible()

    # ================================== Open Project ==================================
    recentProjectsActions[0].trigger()
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)
