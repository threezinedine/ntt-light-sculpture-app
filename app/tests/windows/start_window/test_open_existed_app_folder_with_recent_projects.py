from dataclasses import asdict
import json
import os
import pytest  # type: ignore
from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot
from PyQt6.QtWidgets import QLabel

from constants import (
    APP_DATA_KEY,
    APPLICATION_DATA_FOLDER,
    TEST_APP_DATA_FOLDER,
    APPLICATION_DATA_FILE,
)
from modules.dependency_injection import DependencyContainer


def test_open_existed_app_folder_with_recent_projects(
    qtbot: QtBot,
    fs: FakeFilesystem,
) -> None:
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    appDataFolder = os.path.join(TEST_APP_DATA_FOLDER, APPLICATION_DATA_FOLDER)

    fs.create_dir(appDataFolder)  # type: ignore

    from windows.starting_window import StartingWindow
    from structs.application import Application

    testApplication = Application()
    testApplication.recentProjectFilePaths = {
        "testProject": "testProject.json",
    }
    content = json.dumps(asdict(testApplication))

    fs.create_file(os.path.join(appDataFolder, APPLICATION_DATA_FILE), contents=content)  # type: ignore

    startWindow: StartingWindow = DependencyContainer.GetInstance(
        StartingWindow.__name__
    )
    qtbot.addWidget(startWindow)

    assert startWindow.windowTitle() == "Light Sculpture Studio - v1.0.0"

    hasNoRecentProjectsLabel = startWindow.recentProjectsContainer.findChildren(QLabel)  # type: ignore
    assert hasNoRecentProjectsLabel[0].isVisible() == False  # type: ignore
