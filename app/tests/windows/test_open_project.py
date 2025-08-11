from pyfakefs.fake_filesystem import FakeFilesystem
import pytest  # type: ignore
from pytest_mock import MockerFixture

from structs.application import Application

from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_NEW_PROJECT_PATH,
    TEST_PROJECT_FILE_ERROR_PROJECT_NAME,
)
from tests.windows.helper import (
    ApplicationBuilder,
    FileDialogSetup,
    FixtureBuilder,
    ProjectBuilder,
)
from utils.application import (
    GetApplicationDataFile,
    GetProjectDataFile,
    GetWindowTitle,
)


def test_open_project(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
    mocker: MockerFixture,
    fs: FakeFilesystem,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_PROJECT_FILE_ERROR_PROJECT_NAME)
            .UseErrorProjectFile()
        )
        .AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(ApplicationBuilder())
        .Build()
    )

    # ================================= SYSTEM HEALTH CHECK =================================
    assert mainWindow.windowTitle() == GetWindowTitle()

    # ================================= Open Errored Project =================================
    dialogMock = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")

    fileDialogSetup.SetOutput(
        GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            TEST_PROJECT_FILE_ERROR_PROJECT_NAME,
        )
    )
    mainWindow.ui.openProjectAction.trigger()

    assert dialogMock.call_count == 1
    assert mainWindow.windowTitle() == GetWindowTitle()

    # ================================= Open Valid Project =================================
    fileDialogSetup.SetOutput(
        GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            TEST_NEW_PROJECT_NAME,
        )
    )
    mainWindow.ui.openProjectAction.trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)


def test_open_project_with_current_recent_project(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
):
    mainWindow = (
        fixtureBuilder.AddApplication(ApplicationBuilder())
        .AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME_2))
        .Build()
    )

    fileDialogSetup.SetOutput(
        GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            TEST_NEW_PROJECT_NAME,
        )
    )
    mainWindow.ui.openProjectAction.trigger()

    # ================================= Load test project =================================
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)
    with open(GetApplicationDataFile(), "r") as f:
        application = Application()
        application.FromJson(f.read())

        assert application.recentProjectNames == [TEST_NEW_PROJECT_NAME]
        assert application.recentProjectFilePaths == {
            TEST_NEW_PROJECT_NAME: GetProjectDataFile(
                TEST_NEW_PROJECT_PATH, TEST_NEW_PROJECT_NAME
            )
        }

    # ================================= Load test project using recent projects =================================
    assert len(mainWindow.recentProjectsActions) == 1
    mainWindow.recentProjectsActions[0].trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)

    # ================================= Load test project using recent projects =================================
    assert len(mainWindow.recentProjectsActions) == 1
    mainWindow.recentProjectsActions[0].trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME)
    assert len(mainWindow.recentProjectsActions) == 1

    # ================================= Open another project =================================
    fileDialogSetup.SetOutput(
        GetProjectDataFile(
            TEST_NEW_PROJECT_PATH,
            TEST_NEW_PROJECT_NAME_2,
        )
    )
    mainWindow.ui.openProjectAction.trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_2)
    assert len(mainWindow.recentProjectsActions) == 2
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_2

    # ================================= Choose project 2 again =================================
    mainWindow.recentProjectsActions[0].trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_2)
    assert len(mainWindow.recentProjectsActions) == 2
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_2
