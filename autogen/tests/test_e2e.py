import os
import pytest
import logging
from typing import Generator
from parser.parser import Parser
from utils.template import AutoGenTemplate


class E2EUtil:
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

    def GenerateOutput(self, jinjaFilePath: str) -> str:
        parser = Parser(self.GetInputFileName())
        template = AutoGenTemplate(jinjaFilePath, parser.GenerateTypeConverter())
        result = template.render(parser.data)
        return self.ReformatOutput(result)

    def ReformatOutput(self, result: str) -> str:
        return (
            result.replace("\n", "")
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
def util() -> Generator[E2EUtil, None, None]:
    util = E2EUtil()

    yield util

    util.Cleanup()


def test_bind_function(util: E2EUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        void foo() __attribute__((annotate("python")));
    }
""",
    )

    result = util.GenerateOutput("templates/binding.j2")
    expected = util.ReformatOutput(
        'm.def("foo", &::NTT_NS::foo, "Function foo is not documented");'
    )
    assert expected in result


def test_bind_enum(util: E2EUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        enum class Foo {
            BAR,
            BAZ,
        }
    }
""",
    )

    result = util.GenerateOutput("templates/binding.j2")

    expected = util.ReformatOutput(
        """enum_<::NTT_NS::Foo>(m, "Foo")

    .value("BAR", ::NTT_NS::Foo::BAR)

    .value("BAZ", ::NTT_NS::Foo::BAZ)

    .export_values();"""
    )

    assert expected in result
