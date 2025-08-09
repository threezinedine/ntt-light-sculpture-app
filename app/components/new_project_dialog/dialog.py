import os
from typing import Callable
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QPushButton, QWidget
from PyQt6.QtCore import Qt
from converted_uis.create_new_project_dialog import Ui_CreateNewProjectDialog


class NewProjectDialog(QDialog):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
        acceptCallback: Callable[[str, str], None] | None = None,
    ) -> None:
        super().__init__(parent, flags)

        self.ui = Ui_CreateNewProjectDialog()
        self._acceptCallback: Callable[[str, str], None] | None = acceptCallback
        self._SetupUi()

    def _SetupUi(self) -> None:
        self.ui.setupUi(self)  # type: ignore

        self.ui.projectPathBrowseButton.clicked.connect(self._OpenFolderSearching)
        self.ui.projectNameInput.textChanged.connect(self._UpdateFinalProjectPath)
        self.ui.buttonBox.accepted.connect(self._Accept)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.ui.buttonBox.rejected.connect(self._Cancel)

    def _Accept(self) -> None:
        if self._acceptCallback is None:
            return

        self._acceptCallback(
            self.ui.projectPathInput.text(), self.ui.projectNameInput.text()
        )

    def _Cancel(self) -> None:
        self.ui.projectPathInput.setText("")
        self.ui.projectNameInput.setText("")
        self._UpdateFinalProjectPath()

    def _UpdateFinalProjectPath(self) -> None:
        finalText = f"Project Path: {self._GetFinalProjectDirectory()}"
        self.ui.finalProjectPathLabel.setText(finalText)

        okButton: QPushButton = self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok
        )

        if (
            self.ui.projectPathInput.text() != ""
            and self.ui.projectNameInput.text() != ""
        ):
            okButton.setEnabled(True)
        else:
            okButton.setEnabled(False)

    def _OpenFolderSearching(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Choose Project Folder")

        if directory:
            self.ui.projectPathInput.setText(directory)
            self._UpdateFinalProjectPath()

    def _GetFinalProjectDirectory(self) -> str:
        if self.ui.projectPathInput.text() == "":
            return ""

        return os.path.normpath(
            os.path.join(
                self.ui.projectPathInput.text(), self.ui.projectNameInput.text()
            )
        )
