from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from components.recent_projects.container import RecentProjectsContainer
from converted_uis.starting_window import Ui_StartingWindow
from modules.dependency_injection import DependencyContainer
from modules.dependency_injection.decorators import as_singleton


@as_singleton()
class StartingWindow(QMainWindow):
    def __init__(
        self,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.ui = Ui_StartingWindow()
        self.ui.setupUi(self)  # type: ignore

        self.ui.RecentProjectsLayout.addWidget(
            DependencyContainer.GetInstance(
                RecentProjectsContainer.__name__,
            )
        )
