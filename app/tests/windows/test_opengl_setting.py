from constants import TEST_NEW_PROJECT_NAME
import pytest  # type: ignore
from pytest_mock import MockerFixture
from tests.windows.assertions import OpenGLSettingAssertion, ProjectAssertion
from tests.windows.helper import (
    ApplicationBuilder,
    FixtureBuilder,
    OpenGLSettingBuilder,
    ProjectBuilder,
)
from utils.logger import logger  # type: ignore
from utils.application import GetWindowTitle


def test_default_opengl_setting(fixtureBuilder: FixtureBuilder):
    fixtureBuilder.AddProject(
        ProjectBuilder().Name(TEST_NEW_PROJECT_NAME)
    ).AddApplication(
        ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME)
    ).Build()

    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertOpenGLSetting(
        OpenGLSettingAssertion()
    ).Assert()


def test_modified_draw_edges(fixtureBuilder: FixtureBuilder):
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    mainWindow.openglSettingWidget.ui.drawEdgesCheckbox.setChecked(False)
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME, True)
    assert mainWindow.viewModel.project.openglSetting.drawEdges == False

    logger.debug("Starting undo")
    mainWindow.ui.undoAction.triggered.emit()
    logger.debug("Undo completed")

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME, False)

    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertOpenGLSetting(
        OpenGLSettingAssertion()
    ).Assert()


def test_load_project_then_renderer_will_be_set(
    fixtureBuilder: FixtureBuilder, mocker: MockerFixture
):
    engineMocker = mocker.patch("Engine.Renderer.SetShouldDrawEdges")

    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddOpenGLSetting(OpenGLSettingBuilder().NotDrawEdges())
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    assert engineMocker.call_count == 1
    assert engineMocker.call_args_list[0].args[0] is False

    mainWindow.openglSettingWidget.ui.drawEdgesCheckbox.stateChanged.emit(2)

    print(engineMocker.call_args_list)
    assert engineMocker.call_count == 2
    assert engineMocker.call_args_list[1].args[0] is True
