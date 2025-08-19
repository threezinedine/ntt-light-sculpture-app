from Engine import Position
from constants import TEST_NEW_PROJECT_NAME
import pytest  # type: ignore
from tests.windows.actors import TabWidgetActor
from tests.windows.assertions import OpenGLSettingAssertion, ProjectAssertion
from tests.windows.helper import ApplicationBuilder, FixtureBuilder, ProjectBuilder
from pytest_mock import MockerFixture
from utils.application import GetWindowTitle


def test_draw_opengl_tab_to_move(
    fixtureBuilder: FixtureBuilder,
    mocker: MockerFixture,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    engineMocker = mocker.patch("Engine.Camera.Move")
    setOriginMocker = mocker.patch("Engine.Camera.SetOrigin")

    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    tabWidgetActor.FocusOpenGLTab().DragDown()

    assert engineMocker.call_count >= 2
    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME, True)

    mainWindow.ui.undoAction.triggered.emit()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME, False)

    assert setOriginMocker.call_count == 1
    assert setOriginMocker.call_args[0][0].IsEqual(Position(1, 1, 2))


def test_save_moved_origin(
    fixtureBuilder: FixtureBuilder,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    tabWidgetActor.FocusOpenGLTab().DragDown(
        startPos=(40, 40),
        endPos=(40, 45),
        delay=0.01,
    )
    mainWindow.ui.saveProjectAction.triggered.emit()

    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertOpenGLSetting(
        OpenGLSettingAssertion().AssertOriginNot([1.0, 1.0, 2.0])
    ).Assert()
