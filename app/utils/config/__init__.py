from components.image_preview_widget.image_preview_viewmodel import (
    ImagePreviewViewModel,
)
from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from components.new_project_dialog.dialog import NewProjectDialog
from components.new_project_dialog.viewmodel import NewProjectDialogViewModel
from components.opengl_setting_widget import OpenGLSettingWidget, OpenGLSettingViewModel
from components.project_widget.project_widget import ProjectWidget
from components.project_widget.project_widget_view_model import ProjectWidgetViewModel
from modules.dependency_injection.helper import as_singleton, as_transition
from structs.application import Application
from structs.project import Project
from windows.main_window import MainWindow
from windows.main_window_viewmodel import MainWindowViewModel


def WarningFilter():
    import warnings

    warnings.filterwarnings("ignore", category=DeprecationWarning)


def DependencyInjectionConfig():
    as_singleton(Application)
    as_singleton(Project)

    as_singleton(NewProjectDialogViewModel)
    as_singleton(MainWindowViewModel)

    as_singleton(ProjectWidgetViewModel)
    as_singleton(ProjectWidget)

    as_transition(ImagePreviewViewModel)
    as_transition(ImagePreviewWidget)

    as_singleton(OpenGLSettingViewModel)
    as_singleton(OpenGLSettingWidget)

    as_singleton(NewProjectDialog)
    as_singleton(MainWindow)
