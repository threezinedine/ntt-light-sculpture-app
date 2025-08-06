# ignore the deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import pytest


def pytest_configure(config: pytest.Config):
    pass


from application import LighSculptureApplication


@pytest.fixture(scope="session")
def qapp_cls() -> type[LighSculptureApplication]:
    return LighSculptureApplication
