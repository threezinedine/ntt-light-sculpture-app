from typing import Optional
from PyQt6.QtWidgets import QWidget
from converted_uis.test_widget import Ui_Form


class WidgetView(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)  # type: ignore
