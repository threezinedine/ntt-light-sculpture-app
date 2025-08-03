import os
import sys
import pytest


def pytest_configure(config: pytest.Config) -> None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
