import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow
from converted_uis.main_window import Ui_lightSculptureApplication

print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "Engine"))
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "Engine")
)

from Engine import Logging, LogLevel, EngineLogRecord
from components.openg_widget import OpenGlWidget

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

        Logging.SetLogCallback(self._handleLog)

        Logging.Log(LogLevel.INFO, "Hello, world!")

        # ================= DETERMINE THE PROCESS ID =================
        self.process_id = os.getpid()
        print(f"Process ID: {self.process_id}")
        # ============================================================

        self.ui = Ui_lightSculptureApplication()
        self.ui.setupUi(self)  # type: ignore

        self.ui.centerLayout.addWidget(OpenGlWidget())

    def _handleLog(self, record: EngineLogRecord) -> None:
        print(f"{record.level}: {record.message}")

    def closeEvent(self, a0: QCloseEvent) -> None:
        Logging.SetLogCallback(None)


class LighSculptureApplication(QApplication):
    def __init__(self, argv: list[str]):
        super().__init__(argv)
        self.main_window = LightSculptureMainWindow()


if __name__ == "__main__":
    app = LighSculptureApplication(sys.argv)
    app.main_window.showMaximized()
    sys.exit(app.exec())
