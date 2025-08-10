from components.new_project_dialog.dialog import NewProjectDialog
from components.new_project_dialog.viewmodel import NewProjectDialogViewModel
from modules.dependency_injection.helper import as_singleton
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

    as_singleton(NewProjectDialog)
    as_singleton(MainWindow)
