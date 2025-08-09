import json
import os
from dacite import from_dict
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture

from utils.application import GetApplicationDataFolder, GetApplicationDataFile
from modules.dependency_injection import DependencyContainer
from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER


def test_open_application_without_existed_application_json(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    appDataFolder = GetApplicationDataFolder()
    applicationJsonFile = GetApplicationDataFile()
    defaultApplication = Application()

    infoMocker = mocker.patch("utils.logger.logger.info")

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)

    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    assert fs.exists(appDataFolder)  # type: ignore
    assert infoMocker.call_count == 2

    assert fs.exists(applicationJsonFile)  # type: ignore

    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)
