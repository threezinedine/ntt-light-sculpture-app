from constants import TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_PATH
from tests.windows.actors import ProjectTreeActor
from tests.windows.helper import ApplicationBuilder, FixtureBuilder, ProjectBuilder
from utils.application import GetImageFileNameFromFilePath  # type: ignore


def test_open_tab_when_interact_with_image(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
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

    index = mainWindow.ui.centerTabWidget.currentIndex()

    assert mainWindow.ui.centerTabWidget.tabText(index) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )
