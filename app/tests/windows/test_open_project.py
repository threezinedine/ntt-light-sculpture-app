from datetime import datetime
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest  # type: ignore
from pytest_mock import MockerFixture

from structs.application import Application
from structs.project import Project

from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_NEW_PROJECT_PATH,
    TEST_PROJECT_FILE_ERROR_FOLDER,
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
    GetProjectDataFolder,
    GetWindowTitle,
)


def test_open_project(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
    mocker: MockerFixture,
    fs: FakeFilesystem,
):
    mainWindow = fixtureBuilder.AddApplication(
        ApplicationBuilder().AddAppDataFolder().AddAppDataFile()
    ).Build()

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


def test_open_project_with_current_recent_project(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
):
    mainWindow = (
        fixtureBuilder.AddApplication(
            ApplicationBuilder().AddAppDataFolder().AddAppDataFile()
        )
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
    print("Choose project 2 again")
    mainWindow.recentProjectsActions[0].trigger()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_2)
    assert len(mainWindow.recentProjectsActions) == 2
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_2
