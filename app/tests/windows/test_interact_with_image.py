from constants import TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_PATH
from tests.windows.actors import ProjectTreeActor, TabWidgetActor
from tests.windows.assertions import TabWidgetAssertion
from tests.windows.helper import ApplicationBuilder, FixtureBuilder, ProjectBuilder
from utils.application import GetImageFileNameFromFilePath
from .actors import tabWidgetActor  # type: ignore


def test_open_tab_when_interact_with_image(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder().Name(TEST_NEW_PROJECT_NAME).AddImage(TEST_PNG_IMAGE_PATH)
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)

    projectTreeActor.OpenContextMenuAt(0)
    projectTreeActor.ChooseOpenImageTabAction()

    tabName = GetImageFileNameFromFilePath(TEST_PNG_IMAGE_PATH)

    tabWidgetAssertion = (
        TabWidgetAssertion(mainWindow.ui.centerTabWidget)
        .AssertCurrentTabName(tabName)
        .AssertTabCount(2)
    )

    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget).CloseTabWithName(tabName)

    tabWidgetAssertion.AssertTabCount(1)


def test_cannot_close_the_view_tab(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder().Name(TEST_NEW_PROJECT_NAME).AddImage(TEST_PNG_IMAGE_PATH)
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()

    tabWidgetActor.CloseTabWithName("View")

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(2)

def test_cannont_open_image_tab_multiple_times(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder().Name(TEST_NEW_PROJECT_NAME).AddImage(TEST_PNG_IMAGE_PATH)
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()
    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()
    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(2)