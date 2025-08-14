from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
)
from tests.windows.assertions import ApplicationAssertion, ProjectAssertion
from utils.application import (
    GetProjectDataFolder,
    GetWindowTitle,
)

from .helper import (
    ApplicationBuilder,
    FolderDialogSetup,
    FixtureBuilder,
    ProjectBuilder,
)
from constants import (
    TEST_NEW_PROJECT_NAME,
    TEST_NEW_PROJECT_NAME_2,
    TEST_NEW_PROJECT_NAME_3,
    TEST_NEW_PROJECT_PATH,
)
from windows.main_window import MainWindow
from components.new_project_dialog.dialog import NewProjectDialog


def test_create_a_new_project(
    fixtureBuilder: FixtureBuilder,
    folderDialogSetup: FolderDialogSetup,
):
    NEW_PROJECT_NAME = "Test Project"
    EXSITED_PROJECT_NAME = "Existed Project"

    mainWindow: MainWindow = (
        fixtureBuilder.AddProject(ProjectBuilder().Name(EXSITED_PROJECT_NAME))
        .AddApplication(ApplicationBuilder())
        .Build()
    )

    mainWindow.ui.newProjectAction.trigger()

    assert mainWindow.newProjectDialog.isVisible()

    newProjectDialog: NewProjectDialog = mainWindow.newProjectDialog
    projectDirectoryLabel: QLabel = newProjectDialog.ui.projectDirectoryLabel
    projectPathInput: QLineEdit = newProjectDialog.ui.projectPathInput
    projectNameInput: QLineEdit = newProjectDialog.ui.projectNameInput
    projectPathBrowseButton: QPushButton = newProjectDialog.ui.projectPathBrowseButton
    buttonBox: QDialogButtonBox = newProjectDialog.ui.buttonBox
    okButton: QPushButton = buttonBox.button(QDialogButtonBox.StandardButton.Ok)
    cancelButton: QPushButton = buttonBox.button(QDialogButtonBox.StandardButton.Cancel)

    # ================================= BEGIN CHECK THE PROJECT PATH ==========================
    assert projectDirectoryLabel.text() == ""
    assert projectPathInput.text() == ""
    assert projectPathInput.isReadOnly()
    assert projectNameInput.text() == ""
    assert not projectNameInput.isReadOnly()
    assert mainWindow.windowTitle() == GetWindowTitle()

    # ================================= MODIFY THE PROJECT NAME =================================
    projectNameInput.setText(NEW_PROJECT_NAME)

    assert projectPathInput.text() == ""
    assert projectDirectoryLabel.text() == ""
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= NOT SELECT THE FOLDER =================================
    folderDialogSetup.SetOutput(None)

    projectPathBrowseButton.click()

    assert projectPathInput.text() == ""
    assert projectDirectoryLabel.text() == ""
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= SELECT THE FOLDER =================================
    folderDialogSetup.SetOutput(TEST_NEW_PROJECT_PATH)
    projectPathBrowseButton.click()

    assert projectPathInput.text() == TEST_NEW_PROJECT_PATH
    assert okButton.isEnabled()
    assert cancelButton.isEnabled()
    assert projectDirectoryLabel.text() == GetProjectDataFolder(
        TEST_NEW_PROJECT_PATH, NEW_PROJECT_NAME
    )

    # ================================= MODIFY THE PROJECT NAME =================================
    projectNameInput.setText(NEW_PROJECT_NAME + " 2")

    assert projectNameInput.text() == NEW_PROJECT_NAME + " 2"
    assert projectDirectoryLabel.text() == GetProjectDataFolder(
        TEST_NEW_PROJECT_PATH, NEW_PROJECT_NAME + " 2"
    )

    # ================================= CANNOT CREATE PROJECT IF NAME IS EMPTY ================================
    projectNameInput.setText("")
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= CANNOT CREATE PROJECT IF FOLDER IS EXISTED ================================
    projectNameInput.setText(EXSITED_PROJECT_NAME)

    folderDialogSetup.SetOutput(TEST_NEW_PROJECT_PATH)
    projectPathBrowseButton.click()

    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= CANCEL THE DIALOG RESET EVERYTHING ================================
    cancelButton.click()
    assert not newProjectDialog.isVisible()
    mainWindow.ui.newProjectAction.trigger()

    assert mainWindow.newProjectDialog.isVisible()
    assert projectPathInput.text() == ""
    assert projectNameInput.text() == ""
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    assert projectDirectoryLabel.text() == ""

    # ================================= CLICK THE CREATE BUTTON =================================
    projectNameInput.setText(NEW_PROJECT_NAME)
    projectPathBrowseButton.click()

    folderDialogSetup.SetOutput(TEST_NEW_PROJECT_PATH)
    projectPathBrowseButton.click()

    okButton.click()

    ProjectAssertion(NEW_PROJECT_NAME).AssertImagesCount(0).Assert()

    assert mainWindow.windowTitle() == GetWindowTitle(NEW_PROJECT_NAME)
    assert len(mainWindow.recentProjectsActions) == 1
    assert mainWindow.recentProjectsActions[0].text() == NEW_PROJECT_NAME

    ApplicationAssertion().AssertRecentProjects([NEW_PROJECT_NAME]).Assert()


def test_create_a_new_project_and_it_the_most_recent_project(
    fixtureBuilder: FixtureBuilder,
    folderDialogSetup: FolderDialogSetup,
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

    mainWindow.ui.newProjectAction.trigger()

    mainWindow.newProjectDialog.ui.projectNameInput.setText(TEST_NEW_PROJECT_NAME_3)
    folderDialogSetup.SetOutput(TEST_NEW_PROJECT_PATH)
    mainWindow.newProjectDialog.ui.projectPathBrowseButton.click()
    mainWindow.newProjectDialog.ui.buttonBox.button(
        QDialogButtonBox.StandardButton.Ok
    ).click()

    assert mainWindow.windowTitle() == GetWindowTitle(TEST_NEW_PROJECT_NAME_3)
    assert len(mainWindow.recentProjectsActions) == 3
    assert mainWindow.recentProjectsActions[0].text() == TEST_NEW_PROJECT_NAME_3
