import os
import sys
from PyQt6.QtWidgets import QApplication
from modules.dependency_injection import DependencyContainer
from windows.main_window import MainWindow
import qdarktheme

from utils.logger import engineLogger, logger

from Engine import Logging, LogLevel, EngineLogRecord, Engine

from utils.config import WarningFilter, DependencyInjectionConfig

WarningFilter()


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


def HandleLog(record: EngineLogRecord) -> None:
    if record.level == LogLevel.INFO:
        engineLogger.info(record.message)
    elif record.level == LogLevel.WARNING:
        engineLogger.warning(record.message)
    elif record.level == LogLevel.ERROR:
        engineLogger.error(record.message)
    elif record.level == LogLevel.FATAL:
        engineLogger.fatal(record.message)


def main() -> None:
    engine = Engine()
    engine.Initialize()

    Logging.SetLogCallback(HandleLog)

    app = LighSculptureApplication(sys.argv)
    qdarktheme.setup_theme()

    DependencyInjectionConfig()

    window = DependencyContainer.GetInstance(MainWindow.__name__)
    window.showMaximized()

    ret = app.exec()

    Logging.SetLogCallback(None)
    engine.Finalize()
    logger.info("Closing application")

    sys.exit(ret)


if __name__ == "__main__":
    main()
