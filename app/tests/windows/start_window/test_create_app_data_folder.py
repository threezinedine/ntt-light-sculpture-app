import os

from PyQt6.QtWidgets import QLabel
from constants import APP_DATA_KEY, APPLICATION_DATA_FILE, APPLICATION_DATA_FOLDER
from pytestqt.qtbot import QtBot
from modules.dependency_injection import DependencyContainer
from pyfakefs.fake_filesystem import FakeFilesystem

TEST_APP_DATA_FOLDER = os.path.join("C:/Users/jason", "appdata")


def test_start_window_create_app_data_folder(
    qtbot: QtBot,
    fs: FakeFilesystem,
) -> None:
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    assert os.environ.get(APP_DATA_KEY, None) is not None

    from windows.starting_window import StartingWindow
    from components.recent_projects.container import RecentProjectsContainer

    startWindow: StartingWindow = DependencyContainer.GetInstance(
        StartingWindow.__name__
    )
    qtbot.addWidget(startWindow)
    startWindow.show()
    assert startWindow.isVisible()

    projectDataFolder = os.path.join(TEST_APP_DATA_FOLDER, APPLICATION_DATA_FOLDER)
    applicationFile = os.path.join(projectDataFolder, APPLICATION_DATA_FILE)

    assert os.path.exists(projectDataFolder)
    assert os.path.isdir(projectDataFolder)
    assert os.path.exists(applicationFile)
    assert os.path.isfile(applicationFile)

    assert startWindow.windowTitle() == "Light Sculpture Studio - v1.0.0"

    # check the recent projects is empty
    recentProjects: RecentProjectsContainer = DependencyContainer.GetInstance(
        RecentProjectsContainer.__name__
    )
    hasNoProjectsLabel = recentProjects.findChildren(QLabel)  # type: ignore
    assert len(hasNoProjectsLabel) == 1
