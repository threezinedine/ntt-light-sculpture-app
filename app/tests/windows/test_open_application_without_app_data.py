import os
import pytest  # type: ignore
from pytestqt.qtbot import QtBot
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture

from constants import APP_DATA_KEY
from modules.dependency_injection import DependencyContainer


def test_open_application_without_app_data(
    qtbot: QtBot,
    fs: FakeFilesystem,
    mocker: MockerFixture,
):
    os.environ.pop(APP_DATA_KEY, None)
    fatalMock = mocker.patch("utils.logger.logger.fatal")

    from windows.main_window import MainWindow

    with pytest.raises(EnvironmentError):
        mainWindow: MainWindow = DependencyContainer.GetInstance(MainWindow.__name__)

        qtbot.addWidget(mainWindow)
        mainWindow.show()

        assert mainWindow.isVisible()
        fatalMock.assert_called_once()
