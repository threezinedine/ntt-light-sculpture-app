import os
import sys
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from converted_uis.main_window import Ui_lightSculptureApplication

sys.path.append(
    "C:/Users/Acer/Project/ntt-light-sculpture-app/engine/build/Debug/Debug"
)
from Engine import add, subtract

# ignore the deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class LightSculptureMainWindow(QMainWindow):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super().__init__(parent, flags)

        # ================= DETERMINE THE PROCESS ID =================
        self.process_id = os.getpid()
        print(f"Process ID: {self.process_id}")
        # ============================================================

        self.ui = Ui_lightSculptureApplication()
        self.ui.setupUi(self)

        self.ui.addButton.clicked.connect(lambda: print(add(1, 2)))
        self.ui.subtractButton.clicked.connect(lambda: print(subtract(1, 2)))


class LighSculptureApplication(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.main_window = LightSculptureMainWindow()


if __name__ == "__main__":
    app = LighSculptureApplication(sys.argv)
    app.main_window.showMaximized()
    sys.exit(app.exec_())
