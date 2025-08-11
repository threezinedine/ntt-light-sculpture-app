import pytest  # type: ignore

from utils.application import GetImageFileNameFromFilePath

from .helper import ApplicationBuilder, FileDialogSetup, FixtureBuilder, ProjectBuilder
from constants import TEST_NEW_PROJECT_NAME, TEST_PNG_IMAGE_PATH
from PyQt6.QtCore import Qt


def test_import_image_file(
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
):
    mainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(TEST_NEW_PROJECT_NAME))
        .AddApplication(ApplicationBuilder())
        .Build()
    )

    fileDialogSetup.SetOutput(TEST_PNG_IMAGE_PATH)
    mainWindow.projectWidget.ui.importFileButton.click()

    # ================== checking the image is loadded ==================
    projectTreeView = mainWindow.projectWidget.ui.projectTreeView
    assert projectTreeView.model() is not None
    assert projectTreeView.model().rowCount() == 1

    item = projectTreeView.model().index(0, 0)
    assert item is not None
    assert item.data(Qt.ItemDataRole.DisplayRole) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )

    # # ================== delete the image ==================
    # imageItem = projectTreeView.model().index(0, 0)
    # print(imageItem)
    # assert False
