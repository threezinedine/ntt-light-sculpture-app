# ignore the deprecation warning
from typing import Generator
import warnings

from modules.event_system.event_system import EventSystem


warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest


def pytest_configure(config: pytest.Config):
    pass


from application import LighSculptureApplication


@pytest.fixture(scope="session")
def qapp_cls() -> type[LighSculptureApplication]:
    return LighSculptureApplication


from modules.dependency_injection import DependencyContainer
from tests.windows.helper import appDataSetup, folderDialogSetup  # type: ignore


@pytest.fixture(autouse=True)
def CleanDependencyContainer() -> Generator[None, None, None]:
    DependencyContainer.Clear()
    EventSystem.Clear()
    yield
    DependencyContainer.Clear()
    EventSystem.Clear()
