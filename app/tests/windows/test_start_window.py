import os
from unittest.mock import patch, MagicMock
from typing import Generator
import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from Engine import Application
from modules.dependency_injection import DependencyContainer
from constants import APP_DATA_KEY
from application import LighSculptureApplication
from pytestqt.qtbot import QtBot


@pytest.fixture()
def empty_environ() -> Generator[None, None, None]:
    os.environ.pop(APP_DATA_KEY)
    yield


@pytest.fixture(autouse=True)
def clear_dependency_container(
    qapp_cls: type[LighSculptureApplication],
) -> Generator[None, None, None]:
    DependencyContainer._singletons[Application.__name__] = Application()  # type: ignore

    yield
    DependencyContainer.Clear()


@pytest.fixture()
def configured_app_data_key(
    fs: FakeFilesystem,
) -> Generator[None, FakeFilesystem, None]:
    os.environ[APP_DATA_KEY] = os.path.join("C:/Users/jason", "appdata")  # type: ignore
    yield fs  # type: ignore
    os.environ.pop(APP_DATA_KEY)


@patch("utils.logger.logger.fatal")
def test_start_window_without_app_data_folder(
    fatalMock: MagicMock,
    empty_environ: None,
    qtbot: QtBot,
) -> None:
    assert os.environ.get(APP_DATA_KEY) is None

    with pytest.raises(EnvironmentError):
        from windows.starting_window import StartingWindow

        startWindow = DependencyContainer.GetInstance(StartingWindow.__name__)
        qtbot.addWidget(startWindow)
        startWindow.show()
        assert startWindow.isVisible()

    fatalMock.assert_called_once()
