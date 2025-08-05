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
    expected = util.ReformatOutput(
        'm.def("foo", &::NTT_NS::foo, "Function foo is not documented");'
    )
    assert expected in result


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

    expected = util.ReformatOutput(
        """enum_<::NTT_NS::Foo>(m, "Foo")

    .value("BAR", ::NTT_NS::Foo::BAR)

    .value("BAZ", ::NTT_NS::Foo::BAZ)

    .export_values();"""
    )

    assert expected in result
