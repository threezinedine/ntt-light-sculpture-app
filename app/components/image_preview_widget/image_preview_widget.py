from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from constants import IMAGE_PREVIEW_CHANGED_EVENT_NAME
from converted_uis.image_preview import Ui_ImagePreviewWidget

from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from .image_preview_viewmodel import ImagePreviewViewModel
from utils.logger import logger  # type: ignore


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
        self.viewModel.Index = index
        self.ui = Ui_ImagePreviewWidget()

        self._SetupUI()

    def _SetupUI(self) -> None:
        self.ui.setupUi(self)  # type: ignore

        EventSystem.RegisterEvent(
            IMAGE_PREVIEW_CHANGED_EVENT_NAME,
            self._OnImagePreviewChanged,
        )

        self.ui.imagePreviewLabel.SetImage(self.viewModel.Image)
        self.ui.thresholdSlider.setValue(self.viewModel.Threshold)
        self.ui.thresholdSlider.valueChanged.connect(self._UpdateBinaryImage)
        self.ui.thresholdSlider.sliderReleased.connect(
            self.viewModel.CompleteThresholdModification
        )
        self._UpdateBinaryImage()

    def _OnImagePreviewChanged(self, index: int) -> None:
        if self.viewModel.Index != index:
            return

        self.ui.thresholdSlider.setValue(self.viewModel.Threshold)

    def _UpdateBinaryImage(self) -> None:
        value = self.ui.thresholdSlider.value()
        self.viewModel.Threshold = value

        self.ui.binaryImageLabel.SetImage(
            self.viewModel.GetBinaryImage(value),
            QImage.Format.Format_Grayscale8,
        )
