from asyncio.log import logger  # type: ignore
from pytest_mock import MockerFixture
from constants import (
    DEFAULT_THRESHOLD,
    TEST_NEW_PROJECT_NAME,
    TEST_PNG_IMAGE_PATH,
    TEST_PNG_IMAGE_PATH_2,
    VIEW_TAB_NAME,
)
from tests.windows.actors import ProjectTreeActor, TabWidgetActor
from tests.windows.assertions import ImageMetadataAssertion, TabWidgetAssertion
from tests.windows.helper import (
    ApplicationBuilder,
    FixtureBuilder,
    ImageBuilder,
    ProjectBuilder,
)
from utils.application import (
    GetImageFileNameFromFilePath,
    GetImageFilePath,
    GetTestProjectDataFolder,
)
from utils.images import ConvertToBinary, LoadImage
from .actors import ImagePreviewWidgetActor, MainWindowActor, tabWidgetActor  # type: ignore
from converted_constants import TEST_PNG_IMAGE_NAME
from PIL import Image


def test_open_tab_when_interact_with_image(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
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
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()

    tabWidgetActor.CloseTabWithName(VIEW_TAB_NAME)

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(
        2
    ).AssertImagePreviewWidgetNotEmpty(1)


def test_cannont_open_image_tab_multiple_times(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
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

    tabWidgetActor.CloseTabWithName(TEST_PNG_IMAGE_NAME)
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(1)

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(
        2
    ).AssertImagePreviewWidgetNotEmpty(1)


def test_cannot_open_the_second_image_multiple_times(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH_2))
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    projectTreeActor.OpenContextMenuAt(1).ChooseOpenImageTabAction()
    projectTreeActor.OpenContextMenuAt(1).ChooseOpenImageTabAction()
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(2)


def test_open_image_tab_with_correct_path(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
    mocker: MockerFixture,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    loadedImage = Image.open(TEST_PNG_IMAGE_PATH)

    imageOpenMocker = mocker.patch(
        "PIL.Image.open",
        return_value=loadedImage,
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()

    imageOpenMocker.assert_called_once_with(
        GetImageFilePath(
            GetTestProjectDataFolder(TEST_NEW_PROJECT_NAME), TEST_PNG_IMAGE_NAME
        )
    )


def test_modify_threshold_then_binary_image_is_updated(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    tabWidgetActor: TabWidgetActor,
    imagePreviewWidgetActor: ImagePreviewWidgetActor,
    mainWindowActor: MainWindowActor,
    mocker: MockerFixture,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH))
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    mainWindowActor.SetMainWindow(mainWindow)
    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget)

    loadedImage = ConvertToBinary(LoadImage(TEST_PNG_IMAGE_PATH))

    thresholdSliderValueMocker = mocker.patch(
        "cv2.threshold",
        return_value=loadedImage,
    )

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()
    imagePreviewWidgetActor.SetImagePreviewWidget(
        mainWindow.ui.centerTabWidget.widget(1)  # type: ignore
    )

    imagePreviewWidgetActor.AssertThresholdSliderValue(DEFAULT_THRESHOLD)
    imagePreviewWidgetActor.DragThresholdSlider(123)

    assert thresholdSliderValueMocker.call_count >= 1
    finalThresholdSliderValue = thresholdSliderValueMocker.call_args[0]
    assert finalThresholdSliderValue[1] == 123  # threshold value

    ImageMetadataAssertion(
        TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_NAME
    ).AssertFileExists().AssertThreshold(128)

    mainWindowActor.SaveWindow()

    ImageMetadataAssertion(
        TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_NAME
    ).AssertFileExists().AssertThreshold(123)
