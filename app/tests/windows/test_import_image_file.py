from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMenu
from pytestqt.qtbot import QtBot

from utils.application import GetImageFileNameFromFilePath

from .helper import ApplicationBuilder, FileDialogSetup, FixtureBuilder, ProjectBuilder
from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_PNG_IMAGE_PATH,
    TEST_PNG_IMAGE_PATH_2,
)


def test_import_image_file(
    qtbot: QtBot,
    fixtureBuilder: FixtureBuilder,
    fileDialogSetup: FileDialogSetup,
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
    projectTreeView = mainWindow.projectWidget.ui.projectTreeView
    assert projectTreeView.model() is not None
    assert projectTreeView.model().rowCount() == 1

    item = projectTreeView.model().index(0, 0)
    assert item is not None
    assert item.data(Qt.ItemDataRole.DisplayRole) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )

    # =================== reopen project ===================
    mainWindow.recentProjectsActions[0].trigger()
    assert projectTreeView.model() is not None
    assert projectTreeView.model().rowCount() == 1

    item = projectTreeView.model().index(0, 0)
    assert item is not None
    assert item.data(Qt.ItemDataRole.DisplayRole) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )

    # ================== delete the image ==================
    imageItem = projectTreeView.model().index(0, 0)
    imageItemRect = projectTreeView.visualRect(imageItem)
    print("Clicking on the image")
    qtbot.mouseClick(  # type: ignore
        projectTreeView.viewport(),
        Qt.MouseButton.RightButton,
        pos=imageItemRect.center(),
    )

    qtbot.wait(100)

    contextMenu: QMenu | None = projectTreeView.findChild(QMenu)  # type: ignore

    # ================== assert context menu is shown ==================
    assert contextMenu is not None
    actions = contextMenu.actions()
    action = next((a for a in actions if a.text() == "Delete"), None)
    assert action is not None
    action.trigger()

    # ================== assert image is deleted ==================
    assert projectTreeView.model() is not None
    assert projectTreeView.model().rowCount() == 0


def test_open_with_with_loadded_file(
    fixtureBuilder: FixtureBuilder,
):
    mainWindow = (
        fixtureBuilder.AddProject(
            ProjectBuilder().Name(TEST_NEW_PROJECT_NAME).AddImage(TEST_PNG_IMAGE_PATH)
        )
        .AddApplication(ApplicationBuilder().AddRecentProject(TEST_NEW_PROJECT_NAME))
        .Build()
    )

    projectViewTree = mainWindow.projectWidget.ui.projectTreeView
    assert projectViewTree.model() is not None
    assert projectViewTree.model().rowCount() == 1

    item = projectViewTree.model().index(0, 0)
    assert item is not None
    assert item.data(Qt.ItemDataRole.DisplayRole) == GetImageFileNameFromFilePath(
        TEST_PNG_IMAGE_PATH
    )


def test_delete_1_among_multiple_images(
    fixtureBuilder: FixtureBuilder,
    qtbot: QtBot,
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

    projectViewTree = mainWindow.projectWidget.ui.projectTreeView

    # ================== assert 2 images are loaded ==================
    assert projectViewTree.model() is not None
    assert projectViewTree.model().rowCount() == 2
    assert projectViewTree.model().index(0, 0).data(
        Qt.ItemDataRole.DisplayRole
    ) == GetImageFileNameFromFilePath(TEST_PNG_IMAGE_PATH)
    assert projectViewTree.model().index(1, 0).data(
        Qt.ItemDataRole.DisplayRole
    ) == GetImageFileNameFromFilePath(TEST_PNG_IMAGE_PATH_2)

    # ================== delete the first image ==================
    imageItem = projectViewTree.model().index(0, 0)
    imageItemRect = projectViewTree.visualRect(imageItem)
    qtbot.mouseClick(  # type: ignore
        projectViewTree.viewport(),
        Qt.MouseButton.RightButton,
        pos=imageItemRect.center(),
    )

    qtbot.wait(100)

    contextMenu: QMenu | None = projectViewTree.findChild(QMenu)  # type: ignore

    # ================== assert context menu is shown ==================
    assert contextMenu is not None
    actions = contextMenu.actions()
    action = next((a for a in actions if a.text() == "Delete"), None)
    assert action is not None
    action.trigger()

    # ================== assert image is deleted ==================
    assert projectViewTree.model() is not None
    assert projectViewTree.model().rowCount() == 1
    assert projectViewTree.model().index(0, 0).data(
        Qt.ItemDataRole.DisplayRole
    ) == GetImageFileNameFromFilePath(TEST_PNG_IMAGE_PATH_2)
