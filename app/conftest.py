# ignore the deprecation warning
from typing import Generator
import warnings

from pyfakefs.fake_filesystem import FakeFilesystem

from modules.event_system.event_system import EventSystem
from utils.config import DependencyInjectionConfig


warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest


def pytest_configure(config: pytest.Config):
    pass


from application import LighSculptureApplication


@pytest.fixture(scope="session")
def qapp_cls() -> type[LighSculptureApplication]:
    return LighSculptureApplication


from modules.dependency_injection import DependencyContainer
from tests.windows.helper import (
    folderDialogSetup,  # type: ignore
    fileDialogSetup,  # type: ignore
    fixtureBuilder,  # type: ignore
)

from tests.windows.actors import (
    projectTreeActor,  # type: ignore
    tabWidgetActor,  # type: ignore
    imagePreviewWidgetActor,  # type: ignore
    mainWindowActor,  # type: ignore
)


@pytest.fixture(autouse=True)
def CleanDependencyContainer(fs: FakeFilesystem) -> Generator[None, None, None]:
    DependencyContainer.Clear()
    DependencyInjectionConfig()
    EventSystem.Clear()
    fs.reset()
    yield
    fs.reset()
    DependencyContainer.Clear()
    EventSystem.Clear()
