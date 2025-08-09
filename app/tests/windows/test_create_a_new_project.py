import os
from PyQt6.QtWidgets import (
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
)
from pytest import MonkeyPatch
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem

from modules.dependency_injection import DependencyContainer

from .helper import AppDataSetup
from constants import TEST_NEW_PROJECT_PATH


def test_create_a_new_project(
    qtbot: QtBot,
    appDataSetup: AppDataSetup,
    monkeypatch: MonkeyPatch,
    fs: FakeFilesystem,
):
    from windows.main_window import MainWindow
    from structs.application import Application
    from components.new_project_dialog.dialog import NewProjectDialog

    NEW_PROJECT_NAME = "Test Project"

    appDataSetup.SetupApplicationData(Application())

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    mainWindow.ui.newProjectAction.trigger()

    assert mainWindow.newProjectDialog.isVisible()

    newProjectDialog: NewProjectDialog = mainWindow.newProjectDialog
    finalProjectLabel: QLabel = newProjectDialog.ui.finalProjectPathLabel
    projectPathInput: QLineEdit = newProjectDialog.ui.projectPathInput
    projectNameInput: QLineEdit = newProjectDialog.ui.projectNameInput
    projectPathBrowseButton: QPushButton = newProjectDialog.ui.projectPathBrowseButton
    buttonBox: QDialogButtonBox = newProjectDialog.ui.buttonBox
    okButton: QPushButton = buttonBox.button(QDialogButtonBox.StandardButton.Ok)
    cancelButton: QPushButton = buttonBox.button(QDialogButtonBox.StandardButton.Cancel)

    # ================================= BEGIN CHECK THE PROJECT PATH ==========================
    assert finalProjectLabel.text().strip() == "Project Path:"
    assert projectPathInput.text() == ""
    assert projectPathInput.isReadOnly()
    assert projectNameInput.text() == ""
    assert not projectNameInput.isReadOnly()

    # ================================= MODIFY THE PROJECT NAME =================================
    projectNameInput.setText(NEW_PROJECT_NAME)

    assert projectPathInput.text() == ""
    assert finalProjectLabel.text().strip() == "Project Path:"
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= NOT SELECT THE FOLDER =================================
    monkeypatch.setattr(
        QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: None,  # type: ignore
    )

    projectPathBrowseButton.click()

    assert projectPathInput.text() == ""
    assert finalProjectLabel.text() == "Project Path: "
    assert not okButton.isEnabled()
    assert cancelButton.isEnabled()

    # ================================= SELECT THE FOLDER =================================
    monkeypatch.setattr(
        QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: TEST_NEW_PROJECT_PATH,  # type: ignore
    )
    projectPathBrowseButton.click()

    assert projectPathInput.text() == TEST_NEW_PROJECT_PATH
    assert okButton.isEnabled()
    assert cancelButton.isEnabled()
    assert (
        finalProjectLabel.text()
        == f"Project Path: {os.path.normpath(os.path.join(TEST_NEW_PROJECT_PATH, NEW_PROJECT_NAME))}"
    )

    # ================================= MODIFY THE PROJECT NAME =================================
    projectNameInput.setText(NEW_PROJECT_NAME + " 2")

    assert projectNameInput.text() == NEW_PROJECT_NAME + " 2"
    assert (
        finalProjectLabel.text()
        == f"Project Path: {os.path.normpath(os.path.join(TEST_NEW_PROJECT_PATH, NEW_PROJECT_NAME + ' 2'))}"
    )

    # ================================= CANNOT CREATE PROJECT IF NAME IS EMPTY ================================
    projectNameInput.setText("")
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

    assert finalProjectLabel.text().strip() == "Project Path:"

    # ================================= CLICK THE CREATE BUTTON =================================
    projectNameInput.setText(NEW_PROJECT_NAME)
    projectPathBrowseButton.click()
    okButton.click()

    projectFolder = os.path.normpath(
        os.path.join(TEST_NEW_PROJECT_PATH, NEW_PROJECT_NAME)
    )

    assert fs.exists(projectFolder)  # type: ignore
