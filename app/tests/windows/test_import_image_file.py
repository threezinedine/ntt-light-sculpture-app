from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot
from tests.windows.assertions import ImageMetadataAssertion, ProjectAssertion
from utils.application import GetImageNameBasedOnExistedImageNames
from .actors import ProjectTreeActor

from .helper import (
    ApplicationBuilder,
    FileDialogSetup,
    FixtureBuilder,
    ImageBuilder,
    ProjectBuilder,
)
from constants import (
    DEFAULT_THRESHOLD,
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_PNG_IMAGE_PATH,
    TEST_PNG_IMAGE_PATH_2,
)
from converted_constants import TEST_PNG_IMAGE_NAME, TEST_PNG_IMAGE_NAME_2


def test_import_image_file(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
    projectTreeActor: ProjectTreeActor,
    fs: FakeFilesystem,
):
    mainWindow = (
        fixtureBuilder.AddRealFile(TEST_PNG_IMAGE_PATH)
        .AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME_2))
        .AddApplication(
            ApplicationBuilder()
            .AddRecentProject(TEST_NEW_PROJECT_NAME)
            .AddRecentProject(TEST_NEW_PROJECT_NAME_2)
        )
        .Build()
    )

    fileDialogSetup.SetOutput(TEST_PNG_IMAGE_PATH)
    mainWindow.projectWidget.ui.importFileButton.click()

    # ================== checking the image is loadded ==================
    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME
    ProjectAssertion(TEST_NEW_PROJECT_NAME, fs).AssertImages(
        [TEST_PNG_IMAGE_NAME]
    ).AssertImageLoadded()
    ImageMetadataAssertion(
        TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_NAME
    ).AssertFileExists().AssertThreshold(DEFAULT_THRESHOLD)

    # =================== reopen project ===================
    mainWindow.recentProjectsActions[0].trigger()
    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME

    # ================== delete the image ==================
    projectTreeActor.OpenContextMenuAt(0).ChooseDeleteAction()

    # ================== assert image is deleted ==================
    assert projectTreeActor.NumberOfRows == 0


def test_open_with_with_loadded_file(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
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

    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME


def test_delete_1_among_multiple_images(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
    fs: FakeFilesystem,
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

    # ================== assert 2 images are loaded ==================
    assert projectTreeActor.NumberOfRows == 2
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME
    assert projectTreeActor.GetItemNameAt(1) == TEST_PNG_IMAGE_NAME_2
    ProjectAssertion(TEST_NEW_PROJECT_NAME, fs).AssertImages(
        [TEST_PNG_IMAGE_NAME, TEST_PNG_IMAGE_NAME_2]
    ).AssertImageLoadded()

    # ================== delete the first image ==================
    projectTreeActor.OpenContextMenuAt(0).ChooseDeleteAction()

    # ================== assert image is deleted ==================
    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME_2
    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImages([TEST_PNG_IMAGE_NAME_2])


def test_delete_the_last_image(
    qtbot: QtBot,
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
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
    projectTreeActor.OpenContextMenuAt(1).ChooseDeleteAction()

    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME
    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImages([TEST_PNG_IMAGE_NAME])


def test_automatically_modify_the_name_of_when_import_existed_image_name(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
    projectTreeActor: ProjectTreeActor,
    fs: FakeFilesystem,
    qtbot: QtBot,
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

    fileDialogSetup.SetOutput(TEST_PNG_IMAGE_PATH)
    mainWindow.projectWidget.ui.importFileButton.click()

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)
    assert projectTreeActor.NumberOfRows == 2
    assert projectTreeActor.GetItemNameAt(0) == TEST_PNG_IMAGE_NAME

    NEW_IMAGE_NAME = GetImageNameBasedOnExistedImageNames(
        TEST_PNG_IMAGE_NAME,
        [TEST_PNG_IMAGE_NAME],
    )
    assert projectTreeActor.GetItemNameAt(1) == NEW_IMAGE_NAME

    ImageMetadataAssertion(
        TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_NAME
    ).AssertFileExists().AssertThreshold(DEFAULT_THRESHOLD)

    ImageMetadataAssertion(
        TEST_NEW_PROJECT_NAME, NEW_IMAGE_NAME
    ).AssertFileExists().AssertThreshold(DEFAULT_THRESHOLD)
