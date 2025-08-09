import os
import json
from dataclasses import asdict
from dacite import from_dict
from PyQt6.QtWidgets import QPushButton
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from constants import (
    APP_DATA_KEY,
    APPLICATION_DATA_FOLDER,
    APPLICATION_DATA_FILE,
    TEST_APP_DATA_FOLDER,
    TEST_NON_EXISTED_PROJECT_FOLDER,
)
from modules.dependency_injection import DependencyContainer


def test_open_non_existed_project(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
):
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    appDataFolder = os.path.join(TEST_APP_DATA_FOLDER, APPLICATION_DATA_FOLDER)
    applicationDataFile = os.path.join(appDataFolder, APPLICATION_DATA_FILE)

    fs.create_dir(appDataFolder)  # type: ignore

    from windows.starting_window import StartingWindow
    from structs.application import Application
    from components.recent_projects.item import RecentProjectsItem

    application = Application()
    application.recentProjectFilePaths = {
        "testProject": TEST_NON_EXISTED_PROJECT_FOLDER,
    }
    content = json.dumps(asdict(application))

    fs.create_file(applicationDataFile, contents=content)  # type: ignore

    startingWindow: StartingWindow = DependencyContainer.GetInstance(
        StartingWindow.__name__
    )

    qtbot.addWidget(startingWindow)
    startingWindow.show()

    recentProjectItems = startingWindow.recentProjectsContainer.findChildren(RecentProjectsItem)  # type: ignore

    assert len(recentProjectItems) == 1

    recentProjectNameButtons = recentProjectItems[0].findChildren(QPushButton)  # type: ignore
    assert len(recentProjectNameButtons) == 1
    messageMock = mocker.patch("PyQt6.QtWidgets.QMessageBox.information")
    recentProjectNameButtons[0].click()  # type: ignore
    messageMock.assert_called_once()

    assert recentProjectItems[0].isVisible() == False  # type: ignore

    hasNoRecentProjectsLabel = startingWindow.recentProjectsContainer.hasNoRecentProjectsLabel  # type: ignore
    assert hasNoRecentProjectsLabel.isVisible() == True  # type: ignore

    with open(applicationDataFile, "r") as f:
        loadedApplication = from_dict(data_class=Application, data=json.load(f))
        assert loadedApplication.recentProjectFilePaths == {}
