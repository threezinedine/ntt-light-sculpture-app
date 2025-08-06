import os
from constants import APP_DATA_KEY
from pytestqt.qtbot import QtBot
from modules.dependency_injection import DependencyContainer
from pyfakefs.fake_filesystem import FakeFilesystem


def test_start_window_create_app_data_folder(
    qtbot: QtBot,
    fs: FakeFilesystem,
) -> None:
    os.environ[APP_DATA_KEY] = os.path.join("C:/Users/jason", "appdata")
    assert os.environ.get(APP_DATA_KEY, None) is not None

    from windows.starting_window import StartingWindow

    startWindow = DependencyContainer.GetInstance(StartingWindow.__name__)
    qtbot.addWidget(startWindow)
    startWindow.show()
    assert startWindow.isVisible()

    projectDataFolder = os.path.join("C:/Users/jason", "appdata", "LightSculpture")
    applicationFile = os.path.join(projectDataFolder, "application.json")

    assert os.path.exists(projectDataFolder)
    assert os.path.isdir(projectDataFolder)
    assert os.path.exists(applicationFile)
    assert os.path.isfile(applicationFile)
