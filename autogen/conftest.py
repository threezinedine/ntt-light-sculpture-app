import os
import sys
import pytest
import logging
from typing import Dict, Generator, List
from parser.parser import Parser
from utils.template import AutoGenTemplate
from parser.parser import ParserDataKey, ParserDataType

CLANG_PATH_KEY = "CLANG_PATH"


class AutoGenUtil:
    def __init__(self) -> None:
        pass

    def GetTestOutputFilePath(self) -> str:
        return os.path.join(os.path.dirname(__file__), "test_output.txt")

    def GetInputFileName(self) -> str:
        return os.path.join(os.path.dirname(__file__), "test.h")

    def CreateInputFile(self, content: str) -> None:
        if os.path.exists(self.GetInputFileName()):
            logging.warning(
                f"File {self.GetInputFileName()} already exists, overwriting ..."
            )

        with open(self.GetInputFileName(), "w") as f:
            f.write(content)

    def GetParsedData(self) -> Dict[ParserDataKey, List[ParserDataType]]:
        parser = Parser(self.GetInputFileName())
        return parser.data

    def GenerateOutput(self, jinjaFilePath: str) -> str:
        parser = Parser(self.GetInputFileName())
        template = AutoGenTemplate(jinjaFilePath, parser.GenerateTypeConverter())
        result = template.render(parser.data)
        return result

    def ReformatOutput(self, result: str) -> str:
        return (
            result.strip()
            .replace("\n", "")
            .replace("    .", ".")
            .replace("\t.", ".")
            .replace("   .", ".")
            .replace("  .", ".")
            .replace(" .", ".")
        )

    def Cleanup(self) -> None:
        if os.path.exists(self.GetTestOutputFilePath()):
            os.remove(self.GetTestOutputFilePath())

        if os.path.exists(self.GetInputFileName()):
            os.remove(self.GetInputFileName())


@pytest.fixture(scope="function")
def util() -> Generator[AutoGenUtil, None, None]:
    util = AutoGenUtil()

    yield util

    util.Cleanup()


def pytest_configure(config: pytest.Config) -> None:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    Parser.ConfigClang(os.environ[CLANG_PATH_KEY])
