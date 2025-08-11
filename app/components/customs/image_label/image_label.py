import cv2 as cv
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt


class ImageLabel(QLabel):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.hasContent = False

    def SetImage(self, image: cv.Mat | None) -> None:
        if image is None:
            return

        self.hasContent = True
        imageData = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)  # type: ignore
        self.setPixmap(QPixmap.fromImage(imageData))
