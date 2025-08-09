from pytestqt.qtbot import QtBot

from modules.dependency_injection import DependencyContainer

from .helper import AppDataSetup


def test_create_a_new_project(
    qtbot: QtBot,
    appDataSetup: AppDataSetup,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    appDataSetup.SetupApplicationData(Application())

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    mainWindow.ui.newProjectAction.trigger()

    assert mainWindow.newProjectDialog.isVisible()
