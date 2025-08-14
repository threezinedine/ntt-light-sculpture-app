from asyncio.log import logger  # type: ignore
from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from pytest_mock import MockerFixture
from constants import (
    DEFAULT_THRESHOLD,
    TEST_NEW_PROJECT_NAME,
    TEST_PNG_IMAGE_PATH,
    TEST_PNG_IMAGE_PATH_2,
    VIEW_TAB_NAME,
)
from tests.windows.actors import ProjectTreeActor, TabWidgetActor
from tests.windows.assertions import (
    ImageAssertion,
    ProjectAssertion,
    TabWidgetAssertion,
)
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
    GetWindowTitle,
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

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertCurrentTabName(
        tabName
    ).AssertTabCount(2).Assert()

    tabWidgetActor.SetTabWidget(mainWindow.ui.centerTabWidget).CloseTabWithName(tabName)

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(1)


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
    ).AssertImagePreviewWidgetNotEmpty(1).Assert()


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

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(2).Assert()

    tabWidgetActor.CloseTabWithName(TEST_PNG_IMAGE_NAME)
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(1).Assert()

    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(
        2
    ).AssertImagePreviewWidgetNotEmpty(1).Assert()


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
    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertTabCount(2).Assert()


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

    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImage(
        ImageAssertion(TEST_PNG_IMAGE_NAME).AssertThreshold(DEFAULT_THRESHOLD)
    ).Assert()

    assert mainWindow.windowTitle() == GetWindowTitle(
        TEST_NEW_PROJECT_NAME,
        isModified=True,
    )
    mainWindowActor.SaveWindow()

    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImage(
        ImageAssertion(TEST_PNG_IMAGE_NAME).AssertThreshold(123)
    ).Assert()
    assert mainWindow.windowTitle() == GetWindowTitle(
        TEST_NEW_PROJECT_NAME,
    )


def test_open_project_with_non_default_image_metadata(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(ImageBuilder().ImportPath(TEST_PNG_IMAGE_PATH).SetThreshold(123))
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    assert projectTreeActor.NumberOfRows == 1
    projectTreeActor.OpenContextMenuAt(0).ChooseOpenImageTabAction()

    imagePreviewWidget: ImagePreviewWidget = (
        mainWindow.ui.centerTabWidget.currentWidget()  # type: ignore
    )
    assert imagePreviewWidget.ui.thresholdSlider.value() == 123

    TabWidgetAssertion(mainWindow.ui.centerTabWidget).AssertImagePreviewWidgetNotEmpty(
        1
    ).Assert()
