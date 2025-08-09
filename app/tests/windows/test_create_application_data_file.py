import os
import json
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from dacite import from_dict

from modules.dependency_injection import DependencyContainer
from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER
from utils.application import GetApplicationDataFile, GetApplicationDataFolder


def test_create_application_data_file(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    infoMocker = mocker.patch("utils.logger.logger.info")

    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    fs.create_dir(GetApplicationDataFolder())  # type: ignore

    defaultApplication = Application()

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    applicationJsonFile = GetApplicationDataFile()
    assert fs.exists(applicationJsonFile)  # type: ignore
    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)

    assert infoMocker.call_count == 1
