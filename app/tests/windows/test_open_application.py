import json
from PyQt6.QtGui import QAction
import pytest  # type: ignore
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from dacite import from_dict

from utils.application import GetApplicationDataFile
from .helper import ApplicationBuilder, FixtureBuilder
from structs.application import Application


def test_create_application_data_folder_and_data_file(
    fixtureBuilder: FixtureBuilder,
    mocker: MockerFixture,
):
    warningMocker = mocker.patch("utils.logger.logger.warning")
    fixtureBuilder.AddApplication(ApplicationBuilder().AddErrorAppDataFile()).Build()

    assert warningMocker.call_count == 1
    with open(GetApplicationDataFile(), "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(Application())


def test_open_application_without_app_data(
    mocker: MockerFixture,
    fixtureBuilder: FixtureBuilder,
):
    fatalMock = mocker.patch("utils.logger.logger.fatal")

    with pytest.raises(EnvironmentError):
        fixtureBuilder.AddApplication(
            ApplicationBuilder().NotUseAppDataEnvironmentVariable()
        ).Build()

    fatalMock.assert_called_once()


def test_create_application_without_app_data_file(
    mocker: MockerFixture,
    fixtureBuilder: FixtureBuilder,
    fs: FakeFilesystem,
):
    infoMocker = mocker.patch("utils.logger.logger.info")

    mainWindow = fixtureBuilder.AddApplication(
        ApplicationBuilder().DontAddAppDataFile()
    ).Build()

    applicationJsonFile = GetApplicationDataFile()
    assert fs.exists(applicationJsonFile)  # type: ignore
    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(Application())

    assert infoMocker.call_count == 1

    # ================================= Test Recent Projects =================================
    noProjectAction: QAction = mainWindow.ui.noProjectsAction

    assert noProjectAction.isVisible()
    assert not noProjectAction.isEnabled()


def test_open_application_without_app_data_folder(
    fs: FakeFilesystem,
    mocker: MockerFixture,
    fixtureBuilder: FixtureBuilder,
):
    infoMocker = mocker.patch("utils.logger.logger.info")
    fixtureBuilder.AddApplication(ApplicationBuilder().DontAddAppDataFolder()).Build()

    assert infoMocker.call_count == 2

    applicationJsonFile = GetApplicationDataFile()
    assert fs.exists(applicationJsonFile)  # type: ignore

    with open(applicationJsonFile, "r") as f:
        writtenApplicationJson = from_dict(data_class=Application, data=json.load(f))
        assert writtenApplicationJson.Compare(Application())
