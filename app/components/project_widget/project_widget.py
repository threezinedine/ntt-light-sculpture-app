from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QFileDialog, QWidget
from PyQt6.QtCore import Qt

from constants import LOAD_IMAGE_EVENT_NAME
from modules.event_system.event_system import EventSystem
from .project_widget_view_model import ProjectWidgetViewModel
from converted_uis.project_widget import Ui_ProjectWidget
from modules.dependency_injection.helper import as_dependency


@as_dependency(ProjectWidgetViewModel)
class ProjectWidget(QWidget):
    def __init__(
        self,
        viewModel: ProjectWidgetViewModel,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)
        self.ui = Ui_ProjectWidget()

        self.viewModel = viewModel

        self._SetupUI()

    def _SetupUI(self) -> None:
        self.ui.setupUi(self)  # type: ignore
        self.ui.importFileButton.clicked.connect(self._ImportImageFile)

        self._ShowImages()
        EventSystem.RegisterEvent(LOAD_IMAGE_EVENT_NAME, self._ShowImages)

    def _ImportImageFile(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self, "Import Image File", "", "Image Files (*.png *.jpg *.jpeg)"
        )

        if file:
            self.viewModel.LoadImage(file)

    def _ShowImages(self) -> None:
        projectView = self.ui.projectTreeView
        projectView.setHeaderHidden(True)

        model = QStandardItemModel()
        rootNode = model.invisibleRootItem()

        for item in self.viewModel.ImageItems:
            rootNode.appendRow(item)

        projectView.setModel(model)
