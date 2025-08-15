from constants import TEST_NEW_PROJECT_NAME
import pytest  # type: ignore
from tests.windows.actors import TabWidgetActor
from tests.windows.helper import ApplicationBuilder, FixtureBuilder, ProjectBuilder
from pytest_mock import MockerFixture


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

    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    tabWidgetActor.FocusOpenGLTab().DragDown()

    assert engineMocker.call_count >= 2
