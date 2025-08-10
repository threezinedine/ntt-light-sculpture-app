from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QWidget
from PyQt6.QtCore import Qt

from converted_uis.create_new_project_dialog import Ui_CreateNewProjectDialog
from modules.dependency_injection.helper import as_dependency
from .viewmodel import NewProjectDialogViewModel


@as_dependency(NewProjectDialogViewModel)
class NewProjectDialog(QDialog):
    def __init__(
        self,
        viewModel: NewProjectDialogViewModel,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ) -> None:
        super().__init__(parent, flags)

        self.viewModel = viewModel

        self.ui = Ui_CreateNewProjectDialog()
        self._SetupUi()

    def _SetupUi(self) -> None:
        self.ui.setupUi(self)  # type: ignore

        self.ui.projectPathBrowseButton.clicked.connect(self._OpenFolderSearching)
        self.ui.projectNameInput.textChanged.connect(self._ProjectNameInputChanged)
        self.ui.buttonBox.accepted.connect(self.viewModel.Accept)
        self.ui.buttonBox.rejected.connect(self._Cancel)

        self._UpdateOkButtonState()

    def _Cancel(self) -> None:
        self.ui.projectPathInput.setText("")
        self.ui.projectNameInput.setText("")
        self.viewModel.Cancel()

    def _ProjectNameInputChanged(self) -> None:
        self.viewModel.ProjectName = self.ui.projectNameInput.text()
        self.ui.projectDirectoryLabel.setText(self.viewModel.FinalProjectPath)
        self._UpdateOkButtonState()

    def _UpdateOkButtonState(self) -> None:
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            self.viewModel.CanCreateProject
        )

    def _OpenFolderSearching(self) -> None:
        directory = QFileDialog.getExistingDirectory(self, "Choose Project Folder")

        if directory:
            self.ui.projectPathInput.setText(directory)
            self.viewModel.ProjectPath = directory
            self.ui.projectDirectoryLabel.setText(self.viewModel.FinalProjectPath)
            self._UpdateOkButtonState()
