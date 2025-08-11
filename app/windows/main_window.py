from PyQt6.QtGui import QAction, QKeyEvent
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QWidget
from PyQt6.QtCore import Qt
from functools import partial

from components.new_project_dialog.dialog import NewProjectDialog
from constants import CHANGE_PROJECT_EVENT_NAME, RECENT_PROJECTS_EVENT_NAME
from converted_uis.main_window import Ui_MainWindow
from components.openg_widget import OpenGlWidget
from modules.dependency_injection.helper import as_dependency
from .main_window_viewmodel import MainWindowViewModel
from modules.event_system.event_system import EventSystem


@as_dependency(
    MainWindowViewModel,
    NewProjectDialog,
)
class MainWindow(QMainWindow):
    def __init__(
        self,
        viewModel: MainWindowViewModel,
        newProjectDialog: NewProjectDialog,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.viewModel = viewModel
        self.viewModel.Config()

        self.ui = Ui_MainWindow()
        self.recentProjectsActions: list[QAction] = []
        self.newProjectDialog = newProjectDialog
        self._SetupUI()

    def _SetupUI(self) -> None:
        """
        Called at the end of the constructor for managing the UI.
        """
        self.ui.setupUi(self)  # type: ignore
        self.setWindowTitle(self.viewModel.WindowTitle)
        self.ui.centerLayout.addWidget(OpenGlWidget())
        self.ui.newProjectAction.triggered.connect(self.newProjectDialog.show)
        self.ui.openProjectAction.triggered.connect(self._OpenProjectCallback)
        self._RecentProjectsCallback()

        EventSystem.RegisterEvent(
            CHANGE_PROJECT_EVENT_NAME, self._ChangeProjectCallback
        )

        EventSystem.RegisterEvent(
            RECENT_PROJECTS_EVENT_NAME, self._RecentProjectsCallback
        )

    def _ChangeProjectCallback(self) -> None:
        self.setWindowTitle(self.viewModel.WindowTitle)

    def _OpenProjectCallback(self) -> None:
        options = QFileDialog.Option.ReadOnly

        projectFile, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            "",
            "Project Files (*.json)",
            options=options,
        )

        if projectFile:
            validate = self.viewModel.OpenProject(projectFile)  # type: ignore
            if not validate:
                QMessageBox.information(
                    self,
                    "Open Project",
                    "Failed to open project",
                )

    def _RecentProjectsCallback(self) -> None:
        recentProjects = self.viewModel.RecentProjects

        for action in self.recentProjectsActions:
            action.setParent(None)  # type: ignore
            action.deleteLater()  # type: ignore

        self.recentProjectsActions.clear()

        if len(recentProjects) == 0:
            self.ui.noProjectsAction.setVisible(True)
            return
        else:
            self.ui.noProjectsAction.setVisible(False)

        print("Recent projects", recentProjects)
        assert len(self.recentProjectsActions) == 0

        for projectName, projectFilePath in recentProjects:

            def OpenProject(projectFilePath: str) -> None:
                success = self.viewModel.OpenProject(projectFilePath)
                if not success:
                    QMessageBox.information(
                        self,
                        "Error",
                        f'Project "{projectName}" is invalid',
                    )
                    EventSystem.TriggerEvent(RECENT_PROJECTS_EVENT_NAME)

            action = QAction(projectName, self.ui.recentProjectsMenu)
            action.triggered.connect(
                partial(OpenProject, projectFilePath)  # type: ignore
            )
            self.recentProjectsActions.append(action)
            self.ui.recentProjectsMenu.addAction(action)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(a0)  # type: ignore
