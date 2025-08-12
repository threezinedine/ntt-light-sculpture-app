from PyQt6.QtGui import QAction, QKeyEvent
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QWidget
from PyQt6.QtCore import Qt
from functools import partial

from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from components.new_project_dialog.dialog import NewProjectDialog
from components.project_widget.project_widget import ProjectWidget
from constants import (
    CHANGE_PROJECT_EVENT_NAME,
    OPEN_IMAGE_TAB_EVENT_NAME,
    RECENT_PROJECTS_EVENT_NAME,
)
from converted_uis.main_window import Ui_MainWindow
from modules.dependency_injection.helper import as_dependency
from modules.dependency_injection import DependencyContainer
from .main_window_viewmodel import MainWindowViewModel
from modules.event_system.event_system import EventSystem
from utils.logger import logger  # type: ignore


@as_dependency(
    MainWindowViewModel,
    NewProjectDialog,
    ProjectWidget,
)
class MainWindow(QMainWindow):
    def __init__(
        self,
        viewModel: MainWindowViewModel,
        newProjectDialog: NewProjectDialog,
        projectWidget: ProjectWidget,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Widget,
    ) -> None:
        super().__init__(parent, flags)

        self.viewModel = viewModel
        self.viewModel.Config()

        self.ui = Ui_MainWindow()
        self.recentProjectsActions: list[QAction] = []
        self.newProjectDialog = newProjectDialog
        self.projectWidget = projectWidget
        self._SetupUI()

    def _SetupUI(self) -> None:
        """
        Called at the end of the constructor for managing the UI.
        """
        self.ui.setupUi(self)  # type: ignore
        self.setWindowTitle(self.viewModel.WindowTitle)
        self.ui.newProjectAction.triggered.connect(self.newProjectDialog.show)
        self.ui.openProjectAction.triggered.connect(self._OpenProjectCallback)

        self.ui.projectTreeWidget.setWidget(self.projectWidget)

        self.ui.centerTabWidget.tabCloseRequested.connect(self._OnTabCloseCallback)

        self._RecentProjectsCallback()

        EventSystem.RegisterEvent(
            CHANGE_PROJECT_EVENT_NAME, self._ChangeProjectCallback
        )

        EventSystem.RegisterEvent(
            RECENT_PROJECTS_EVENT_NAME, self._RecentProjectsCallback
        )
        EventSystem.RegisterEvent(OPEN_IMAGE_TAB_EVENT_NAME, self._OpenImageTabCallback)

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

        self.recentProjectsActions.clear()

        if len(recentProjects) == 0:
            self.ui.noProjectsAction.setVisible(True)
            return
        else:
            self.ui.noProjectsAction.setVisible(False)

        assert len(self.recentProjectsActions) == 0

        for projectName, projectFilePath in recentProjects:

            def OpenProject(projectName: str, projectFilePath: str) -> None:
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
                partial(OpenProject, projectName, projectFilePath)  # type: ignore
            )
            self.recentProjectsActions.append(action)
            self.ui.recentProjectsMenu.addAction(action)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(a0)  # type: ignore

    def _OpenImageTabCallback(self, row: int) -> None:
        logger.debug(f"Open Image Tab Callback: {row}")
        for i in range(self.ui.centerTabWidget.count()):
            if (
                self.ui.centerTabWidget.tabText(i)
                == self.projectWidget.viewModel.ImageItems[row].text()
            ):
                self.ui.centerTabWidget.setCurrentWidget(
                    self.ui.centerTabWidget.widget(i)
                )
                return

        imagePreviewWidget: ImagePreviewWidget = DependencyContainer.GetInstance(
            ImagePreviewWidget.__name__,
            row,
        )

        centerTabWidget = self.ui.centerTabWidget
        centerTabWidget.addTab(imagePreviewWidget, imagePreviewWidget.viewModel.TabName)  # type: ignore
        centerTabWidget.setCurrentWidget(imagePreviewWidget)

    def _OnTabCloseCallback(self, index: int) -> None:
        centerTabWidget = self.ui.centerTabWidget

        widget = centerTabWidget.widget(index)

        if widget and isinstance(widget, ImagePreviewWidget):
            centerTabWidget.removeTab(index)
