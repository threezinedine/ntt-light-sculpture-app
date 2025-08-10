import os
import json
from PyQt6.QtGui import QAction
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from dacite import from_dict

from constants import APP_DATA_KEY, TEST_APP_DATA_FOLDER
from utils.application import GetApplicationDataFile, GetApplicationDataFolder
from .helper import AppDataSetup, MainWindowBuilder
from structs.application import Application


def test_create_application_data_folder_and_data_file(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
    appDataSetup: AppDataSetup,
    mainWindowBuilder: MainWindowBuilder,
):
    warningMocker = mocker.patch("utils.logger.logger.warning")
    defaultApplication = Application()

    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER

    with open(GetApplicationDataFile(), "w") as f:
        f.write('{"Error"}')

    mainWindowBuilder.Build()

    assert warningMocker.call_count == 1
    with open(GetApplicationDataFile(), "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)


def test_open_application_without_app_data(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
    mainWindowBuilder: MainWindowBuilder,
):
    os.environ.pop(APP_DATA_KEY, None)
    fatalMock = mocker.patch("utils.logger.logger.fatal")

    with pytest.raises(EnvironmentError):
        mainWindowBuilder.Build()

    fatalMock.assert_called_once()


def test_create_application_data_file(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
    mainWindowBuilder: MainWindowBuilder,
):
    from windows.main_window import MainWindow
    from structs.application import Application

    infoMocker = mocker.patch("utils.logger.logger.info")

    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    if not fs.exists(GetApplicationDataFolder()):  # type: ignore
        fs.create_dir(GetApplicationDataFolder())  # type: ignore

    defaultApplication = Application()

    mainWindow: MainWindow = mainWindowBuilder.Build()

    applicationJsonFile = GetApplicationDataFile()
    assert fs.exists(applicationJsonFile)  # type: ignore
    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)

    assert infoMocker.call_count == 1

    # ================================= Test Recent Projects =================================
    noProjectAction: QAction = mainWindow.ui.noProjectsAction

    assert noProjectAction.isVisible()
    assert not noProjectAction.isEnabled()


def test_open_application_without_existed_application_json(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
    mainWindowBuilder: MainWindowBuilder,
):
    fs.reset()
    os.environ[APP_DATA_KEY] = TEST_APP_DATA_FOLDER
    appDataFolder = GetApplicationDataFolder()

    applicationJsonFile = GetApplicationDataFile()
    defaultApplication = Application()

    infoMocker = mocker.patch("utils.logger.logger.info")

    mainWindowBuilder.Build()

    assert fs.exists(appDataFolder)  # type: ignore
    assert infoMocker.call_count == 2

    assert fs.exists(applicationJsonFile)  # type: ignore

    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(defaultApplication)
