from PyQt6.QtGui import QAction
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem

from constants import TEST_NEW_PROJECT_NAME, TEST_NEW_PROJECT_PATH
from modules.dependency_injection import DependencyContainer
from tests.windows.helper import AppDataSetup, ProjectSetup
from utils.application import GetProjectDataFile


def test_recent_projects_feature(
    qtbot: QtBot,
    fs: FakeFilesystem,
    appDataSetup: AppDataSetup,
    projectSetup: ProjectSetup,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    projectSetup.SetupProjectData(TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME)

    application = Application()
    application.recentProjectFilePaths[TEST_NEW_PROJECT_NAME] = GetProjectDataFile(
        TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME
    )
    appDataSetup.SetupApplicationData(application)

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    noProjectAction: QAction = mainWindow.ui.noProjectsAction

    # ================================= Test No Project =================================
    assert not noProjectAction.isVisible()
