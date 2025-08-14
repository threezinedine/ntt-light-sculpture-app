from pytest_mock import MockerFixture
from tests.windows.assertions import ApplicationAssertion
from tests.windows.helper import ApplicationBuilder, FixtureBuilder, ProjectBuilder
from constants import TEST_NEW_PROJECT_NAME, TEST_NEW_PROJECT_NAME_2
from utils.application import GetTestProjectDataFolder


def test_wrong_application_json(fixtureBuilder: FixtureBuilder, mocker: MockerFixture):
    infoMocker = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    mainWindow = fixtureBuilder.AddApplication(
        ApplicationBuilder()
        .AddErrorRecentProject(
            TEST_NEW_PROJECT_NAME_2,
            GetTestProjectDataFolder(TEST_NEW_PROJECT_NAME_2),
        )
        .AddRecentProject(TEST_NEW_PROJECT_NAME)
    ).Build()

    assert len(mainWindow.recentProjectsActions) == 1
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME

    ApplicationAssertion().AssertRecentProjects([TEST_NEW_PROJECT_NAME]).Assert()
    infoMocker.assert_called_once()


def test_choose_wrong_recent_project_file(
    fixtureBuilder: FixtureBuilder, mocker: MockerFixture
):
    infoMocker = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(
            ApplicationBuilder()
            .AddRecentProject(TEST_NEW_PROJECT_NAME)
            .AddErrorRecentProject(
                TEST_NEW_PROJECT_NAME_2,
                GetTestProjectDataFolder(TEST_NEW_PROJECT_NAME_2),
            )
        )
        .Build()
    )

    assert len(mainWindow.recentProjectsActions) == 2

    mainWindow.recentProjectsActions[1].trigger()

    infoMocker.assert_called_once()

    assert len(mainWindow.recentProjectsActions) == 1
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME
