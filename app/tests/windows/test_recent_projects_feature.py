from PyQt6.QtGui import QAction
import pytest  # type: ignore

from constants import (
    MAX_NUMBER_OF_RECENT_PROJECTS,
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_NEW_PROJECT_NAME_3,
    TEST_NEW_PROJECT_NAME_4,
    TEST_NEW_PROJECT_NAME_5,
    TEST_NEW_PROJECT_NAME_6,
    TEST_NEW_PROJECT_PATH,
)
from structs.application import Application
from tests.windows.helper import FileDialogSetup, FixtureBuilder
from utils.application import GetApplicationDataFile, GetProjectDataFile, GetWindowTitle


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


def test_only_has_maximum_5_recent_projects(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
):
    mainWindow = (
        fixtureBuilder.UseAppDataApplication()
        .AddAppDataFolder()
        .AddAppDataFile()
        .AddProject(TEST_NEW_PROJECT_NAME)
        .AddProject(TEST_NEW_PROJECT_NAME_2)
        .AddProject(TEST_NEW_PROJECT_NAME_3)
        .AddProject(TEST_NEW_PROJECT_NAME_4)
        .AddProject(TEST_NEW_PROJECT_NAME_5)
        .AddProject(TEST_NEW_PROJECT_NAME_6)
        .AddRecentProject(TEST_NEW_PROJECT_NAME)
        .AddRecentProject(TEST_NEW_PROJECT_NAME_2)
        .AddRecentProject(TEST_NEW_PROJECT_NAME_3)
        .AddRecentProject(TEST_NEW_PROJECT_NAME_4)
        .AddRecentProject(TEST_NEW_PROJECT_NAME_5)
        .AddRecentProject(TEST_NEW_PROJECT_NAME_6)
        .Build()
    )

    assert len(mainWindow.recentProjectsActions) == MAX_NUMBER_OF_RECENT_PROJECTS
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME

    # ===================== Open project on the list ================================
    mainWindow.recentProjectsActions[3].trigger()  # PROJECT 4
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_4)
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_4
    assert mainWindow.recentProjectsActions[1].text() == TEST_NEW_PROJECT_NAME
    assert mainWindow.recentProjectsActions[2].text() == TEST_NEW_PROJECT_NAME_2
    assert mainWindow.recentProjectsActions[3].text() == TEST_NEW_PROJECT_NAME_3
    assert mainWindow.recentProjectsActions[4].text() == TEST_NEW_PROJECT_NAME_5

    # ===================== Open project outside the list ================================
    fileDialogSetup.SetOutput(
        GetProjectDataFile(TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME_6)
    )
    mainWindow.ui.openProjectAction.trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_6)
    assert len(mainWindow.recentProjectsActions) == MAX_NUMBER_OF_RECENT_PROJECTS
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_6
    assert mainWindow.recentProjectsActions[1].text() == TEST_NEW_PROJECT_NAME_4
    assert mainWindow.recentProjectsActions[2].text() == TEST_NEW_PROJECT_NAME
    assert mainWindow.recentProjectsActions[3].text() == TEST_NEW_PROJECT_NAME_2
    assert mainWindow.recentProjectsActions[4].text() == TEST_NEW_PROJECT_NAME_3

    # ===================== Checking the application data file ================================
    with open(GetApplicationDataFile(), "r") as f:
        application = Application()
        application.FromJson(f.read())

        targetRecentProjectNames = [
            TEST_NEW_PROJECT_NAME_6,
            TEST_NEW_PROJECT_NAME_4,
            TEST_NEW_PROJECT_NAME,
            TEST_NEW_PROJECT_NAME_2,
            TEST_NEW_PROJECT_NAME_3,
        ]

        assert application.recentProjectNames == targetRecentProjectNames
        assert set(application.recentProjectFilePaths.keys()) == set(
            targetRecentProjectNames
        )
