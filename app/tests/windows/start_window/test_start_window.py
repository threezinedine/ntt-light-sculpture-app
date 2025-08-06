import os
from unittest.mock import patch, MagicMock
import pytest
from modules.dependency_injection import DependencyContainer
from constants import APP_DATA_KEY
from pytestqt.qtbot import QtBot


@patch("utils.logger.logger.fatal")
def test_start_window_without_app_data_folder(
    fatalMock: MagicMock,
    qtbot: QtBot,
) -> None:
    os.environ.pop(APP_DATA_KEY, None)

    assert os.environ.get(APP_DATA_KEY, None) is None

    with pytest.raises(EnvironmentError):
        from windows.starting_window import StartingWindow

        startWindow = DependencyContainer.GetInstance(StartingWindow.__name__)
        qtbot.addWidget(startWindow)
        startWindow.show()
        assert startWindow.isVisible()

    fatalMock.assert_called_once()
