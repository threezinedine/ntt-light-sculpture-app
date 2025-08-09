import os
import json
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from dacite import from_dict

from modules.dependency_injection import DependencyContainer
from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER
from utils.application import GetApplicationDataFile
from .helper import AppDataSetup


def test_create_application_data_file(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
    appDataSetup: AppDataSetup,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    warningMocker = mocker.patch("utils.logger.logger.warning")
    defaultApplication = Application()

    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER

    with open(GetApplicationDataFile(), "w") as f:
        f.write('{"Error"}')

    mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)
    qtbot.addWidget(mainWindow)
    mainWindow.showMaximized()

    assert warningMocker.call_count == 1
    with open(GetApplicationDataFile(), "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)
