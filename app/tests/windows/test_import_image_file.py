from tests.windows.assertions import ProjectAssertion
from .actors import ProjectTreeActor
from utils.application import GetImageFileNameFromFilePath

from .helper import ApplicationBuilder, FileDialogSetup, FixtureBuilder, ProjectBuilder
from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_PNG_IMAGE_PATH,
    TEST_PNG_IMAGE_PATH_2,
)


def test_import_image_file(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
    projectTreeActor: ProjectTreeActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
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
    assert projectTreeActor.GetItemNameAt(0) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )
    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImages([TEST_PNG_IMAGE_PATH])

    # =================== reopen project ===================
    mainWindow.recentProjectsActions[0].trigger()
    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )

    # ================== delete the image ==================
    projectTreeActor.OpenContextMenuAt(0).DeleteImage()

    # ================== assert image is deleted ==================
    assert projectTreeActor.NumberOfRows == 0


def test_open_with_with_loadded_file(
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

    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )


def test_delete_1_among_multiple_images(
    fixtureBuilder: FixtureBuilder,
    projectTreeActor: ProjectTreeActor,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder()
            .Name(TEST_NEW_PROJECT_NAME)
            .AddImage(TEST_PNG_IMAGE_PATH)
            .AddImage(TEST_PNG_IMAGE_PATH_2)
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectTreeActor.SetProjectTreeView(mainWindow.projectWidget.ui.projectTreeView)

    # ================== assert 2 images are loaded ==================
    assert projectTreeActor.NumberOfRows == 2
    assert projectTreeActor.GetItemNameAt(0) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )
    assert projectTreeActor.GetItemNameAt(1) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH_2
    )
    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImages(
        [TEST_PNG_IMAGE_PATH, TEST_PNG_IMAGE_PATH_2]
    )

    # ================== delete the first image ==================
    projectTreeActor.OpenContextMenuAt(0).DeleteImage()

    # ================== assert image is deleted ==================
    assert projectTreeActor.NumberOfRows == 1
    assert projectTreeActor.GetItemNameAt(0) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH_2
    )
    ProjectAssertion(TEST_NEW_PROJECT_NAME).AssertImages([TEST_PNG_IMAGE_PATH_2])
