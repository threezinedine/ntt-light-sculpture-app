from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt
from converted_uis.create_new_project_dialog import Ui_CreateNewProjectDialog


class NewProjectDialog(QDialog):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ) -> None:
        super().__init__(parent, flags)

        self.ui = Ui_CreateNewProjectDialog()
        self._SetupUi()

    def _SetupUi(self) -> None:
        self.ui.setupUi(self)  # type: ignore
