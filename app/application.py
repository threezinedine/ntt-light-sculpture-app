import os
import sys
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication
from modules.dependency_injection import DependencyContainer
from utils.logger import engineLogger, logger

print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "Engine"))
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "Engine")
)

from Engine import Logging, LogLevel, EngineLogRecord

# ignore the deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


class LighSculptureApplication(QApplication):
    def __init__(
        self,
        argv: list[str] = sys.argv,
    ):
        super().__init__(argv)

        # ================= DETERMINE THE PROCESS ID =================
        self.process_id = os.getpid()
        logger.info(f"Process ID: {self.process_id}")
        # ============================================================

        Logging.SetLogCallback(self._handleLog)

    def _handleLog(self, record: EngineLogRecord) -> None:
        if record.level == LogLevel.INFO:
            engineLogger.info(record.message)
        elif record.level == LogLevel.WARNING:
            engineLogger.warning(record.message)
        elif record.level == LogLevel.ERROR:
            engineLogger.error(record.message)
        elif record.level == LogLevel.FATAL:
            engineLogger.fatal(record.message)

    def closeEvent(self, a0: QCloseEvent) -> None:
        Logging.SetLogCallback(None)
        logger.info("Closing application")


def main() -> None:
    app = LighSculptureApplication(sys.argv)

    from windows.starting_window import StartingWindow

    window = DependencyContainer.GetInstance(StartingWindow.__name__)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
