import os
import sys
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication
from modules.dependency_injection import DependencyContainer
from utils.logger import engineLogger, logger

from Engine import Logging, LogLevel, EngineLogRecord, Engine

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
        self.engine = Engine()
        self.engine.Initialize()

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
        self.engine.Finalize()
        logger.info("Closing application")


def main() -> None:
    app = LighSculptureApplication(sys.argv)

    from windows.main_window import MainWindow

    window = DependencyContainer.GetInstance(MainWindow.__name__)
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input()
