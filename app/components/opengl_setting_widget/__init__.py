from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from constants import OPENGL_SETTING_CHANGED_EVENT_NAME
from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from .opengl_setting_viewmodel import OpenGLSettingViewModel
from converted_uis.opengl_setting import Ui_OpenGLSettingWidget


@as_dependency(OpenGLSettingViewModel)
class OpenGLSettingWidget(QWidget):
    def __init__(
        self,
        viewModel: OpenGLSettingViewModel,
        parent: QWidget | None = None,
        flags: Qt.WindowType = Qt.WindowType.Window,
    ) -> None:
        super().__init__(parent, flags)
        self.viewModel = viewModel

        self.ui = Ui_OpenGLSettingWidget()

        self._inUpdate: bool = False
        self._SetupUI()

    def _SetupUI(self) -> None:
        self.ui.setupUi(self)  # type: ignore

        self._UpdateInfo()
        EventSystem.RegisterEvent(OPENGL_SETTING_CHANGED_EVENT_NAME, self._UpdateInfo)

        self.ui.drawEdgesCheckbox.stateChanged.connect(self._OnDrawEdgesChanged)
        self.ui.drawFacesCheckbox.stateChanged.connect(self._OnDrawFacesChanged)

    def _UpdateInfo(self) -> None:
        self._inUpdate = True
        self.ui.drawEdgesCheckbox.setChecked(self.viewModel.DrawEdges)
        self.ui.drawFacesCheckbox.setChecked(self.viewModel.DrawFaces)
        self._inUpdate = False

    def _OnDrawEdgesChanged(self, state: int) -> None:
        self.viewModel.SetDrawEdges(
            state == Qt.CheckState.Checked,
            propagate=not self._inUpdate,
        )

    def _OnDrawFacesChanged(self, state: int) -> None:
        self.viewModel.SetDrawFaces(
            state == Qt.CheckState.Checked,
            propagate=not self._inUpdate,
        )
