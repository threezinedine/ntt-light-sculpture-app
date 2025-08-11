from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from converted_uis.image_preview import Ui_ImagePreviewWidget
from modules.dependency_injection.helper import as_dependency
from .image_preview_viewmodel import ImagePreviewViewModel


@as_dependency(ImagePreviewViewModel)
class ImagePreviewWidget(QWidget):
    def __init__(
        self,
        viewmodel: ImagePreviewViewModel,
        index: int = 0,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super().__init__(parent, flags)
        self.viewModel = viewmodel
        self.ui = Ui_ImagePreviewWidget()

        self._SetupUI()

    def _SetupUI(self) -> None:
        self.ui.setupUi(self)  # type: ignore
