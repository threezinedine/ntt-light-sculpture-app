from unittest.mock import MagicMock, patch
from conftest import AutoGenUtil


def test_bind_function(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        void foo() __attribute__((annotate("python")));
    }
""",
    )

    result = util.GenerateOutput("templates/binding.j2")
    expected = 'm.def("foo", &::NTT_NS::foo, "Function foo is not documented");'
    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


def test_bind_enum(util: AutoGenUtil) -> None:
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

    expected = """enum_<::NTT_NS::Foo>(m, "Foo")

    .value("BAR", ::NTT_NS::Foo::BAR)

    .value("BAZ", ::NTT_NS::Foo::BAZ)

    .export_values();"""

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


def test_bind_typedef(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        typedef Function<void, const EngineLogRecord &> LogCallback;
    }
""",
    )

    result = util.GenerateOutput("templates/pyi_binding.j2")

    expected = """
        LogCallback: TypeAlias = Callable[["EngineLogRecord"], None]
    """

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


@patch("utils.types.logger.warning")
def test_bind_typedef_without_self_defined_type(
    mockWarning: MagicMock,
    util: AutoGenUtil,
) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        typedef Function<void, const EngineLogRecord &> NonDefinedType;
    }
""",
    )

    result = util.GenerateOutput("templates/pyi_binding.j2")

    expected = """
        NonDefinedType: TypeAlias = Any
    """

    mockWarning.assert_called_once()

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)
