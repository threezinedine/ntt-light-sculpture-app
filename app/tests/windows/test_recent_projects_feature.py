from PyQt6.QtGui import QAction
import pytest  # type: ignore

from constants import TEST_NEW_PROJECT_NAME
from tests.windows.helper import FixtureBuilder
from utils.application import GetWindowTitle


def test_recent_projects_feature(
    fixtureBuilder: FixtureBuilder,
):
    mainWindow = (
        fixtureBuilder.UseAppDataApplication()
        .AddAppDataFolder()
        .AddAppDataFile()
        .AddProject(TEST_NEW_PROJECT_NAME)
        .AddRecentProject(TEST_NEW_PROJECT_NAME)
        .Build()
    )

    noProjectAction: QAction = mainWindow.ui.noProjectsAction
    recentProjectsActions: list[QAction] = mainWindow.recentProjectsActions

    # ================================= Test No Project =================================
    assert not noProjectAction.isVisible()
    assert len(recentProjectsActions) == 1
    assert recentProjectsActions[0].isVisible()

    # ================================== Open Project ==================================
    recentProjectsActions[0].trigger()
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)
