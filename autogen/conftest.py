import os
import sys
import pytest
from parser.parser import Parser

CLANG_PATH_KEY = "CLANG_PATH"


def pytest_configure(config: pytest.Config) -> None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    Parser.ConfigClang(os.environ[CLANG_PATH_KEY])
