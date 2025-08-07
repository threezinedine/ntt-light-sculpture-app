from dataclasses import asdict
import os
import pytest  # type: ignore
from pyfakefs.fake_filesystem import FakeFilesystem
from PyQt6.QtWidgets import QLabel

import json

from pytestqt.qtbot import QtBot
from constants import (
    APP_DATA_KEY,
    APPLICATION_DATA_FOLDER,
    TEST_APP_DATA_FOLDER,
    APPLICATION_DATA_FILE,
)
from modules.dependency_injection import DependencyContainer


def test_start_window_with_existed_project_file(
    fs: FakeFilesystem,
    qtbot: QtBot,
) -> None:
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    fs.create_dir(TEST_APP_DATA_FOLDER)  # type: ignore
    appDataFolder = os.path.join(TEST_APP_DATA_FOLDER, APPLICATION_DATA_FOLDER)
    fs.create_dir(appDataFolder)  # type: ignore
    from windows.starting_window import StartingWindow
    from structs.application import Application
    from structs.version import Version

    testApplication = Application()
    testApplication.version = Version(1, 0, 1)

    content = json.dumps(asdict(testApplication))

    fs.create_file(os.path.join(appDataFolder, APPLICATION_DATA_FILE), contents=content)  # type: ignore

    assert os.environ.get(APP_DATA_KEY, None) is not None

    startWindow: StartingWindow = DependencyContainer.GetInstance(
        StartingWindow.__name__
    )
    qtbot.addWidget(startWindow)

    assert startWindow.windowTitle() == "Light Sculpture Studio - v1.0.1"

    hasNoProjectsLabels = startWindow.recentProjectsContainer.findChildren(QLabel)  # type: ignore
    assert len(hasNoProjectsLabels) == 1
