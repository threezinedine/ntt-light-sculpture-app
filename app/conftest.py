# ignore the deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def pytest_configure(config):
    pass
