from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from converted_uis.main_window import Ui_MainWindow
from components.openg_widget import OpenGlWidget


class MainWindow(QMainWindow):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # type: ignore

        self.ui.centerLayout.addWidget(OpenGlWidget())
