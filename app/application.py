import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from converted_uis.main_window import Ui_lightSculptureApplication

sys.path.append(
    "C:/Users/Acer/Project/ntt-light-sculpture-app/engine/build/Debug/Debug"
)
from Engine import add

# ignore the deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

print(add(1, 2))


class LightSculptureMainWindow(QMainWindow):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ):
        super().__init__(parent, flags)
        self.ui = Ui_lightSculptureApplication()
        self.ui.setupUi(self)


class LighSculptureApplication(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.main_window = LightSculptureMainWindow()


if __name__ == "__main__":
    app = LighSculptureApplication(sys.argv)
    app.main_window.showMaximized()
    sys.exit(app.exec_())
