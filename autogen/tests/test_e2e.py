from unittest.mock import MagicMock, patch

import pytest  # type: ignore
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
        LogCallback: TypeAlias = Union[Callable[["EngineLogRecord"], None], None]
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


def test_bind_struct_without_constructor(
    util: AutoGenUtil,
) -> None:
    util.CreateInputFile(
        """
    namespace ntt 
    {
        struct __attribute__((annotate("python"))) Engine {
            int a;
            int b;
        };
    }
"""
    )

    result = util.GenerateOutput("templates/binding.j2")

    expected = """
        class_<::NTT_NS::Engine>(m, "Engine")
            .def(init<>())
            .def_readwrite("a", &::NTT_NS::Engine::a)
            .def_readwrite("b", &::NTT_NS::Engine::b);
"""

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


def test_not_bind_struct_without_annotation(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        struct Engine {
            int a;
            int b;
        };
    }
"""
    )

    result = util.GenerateOutput("templates/binding.j2")

    expected = """
        class_<::NTT_NS::Engine>(m, "Engine")
            .def(init<>())
            .def_readwrite("a", &::NTT_NS::Engine::a)
            .def_readwrite("b", &::NTT_NS::Engine::b);
"""

    assert util.ReformatOutput(expected) not in util.ReformatOutput(result)


def test_convert_position_to_python(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        class __attribute__((annotate("python"))) Position {
        public:
            Position(float x, float y, float z) : m_data(x, y, z) {}
            Position(const Position &other) : m_data(other.m_data) {}
            ~Position() {}

            inline float x() __attribute__((annotate("python"))) const;
            inline float y() __attribute__((annotate("python"))) const;
            inline float z() __attribute__((annotate("python"))) const;

        private:
            glm::vec3 m_data;
        };
    }
"""
    )

    result = util.GenerateOutput("templates/binding.j2")

    expected = """
        class_<::NTT_NS::Position>Position_Obj(m, "Position");
        Position_Obj
            .def(init<float, float, float>())
            .def(init<const Position &>())
            .def("x", &::NTT_NS::Position::x, "Method x is not documented")
            .def("y", &::NTT_NS::Position::y, "Method y is not documented")
            .def("z", &::NTT_NS::Position::z, "Method z is not documented");
"""

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


def test_binding_position_to_pyi(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        class __attribute__((annotate("python"))) Position {
        public:
            Position(float x, float y, float z) : m_data(x, y, z) {}
            Position(const Position &other) : m_data(other.m_data) {}
            ~Position() {}

            inline float x() __attribute__((annotate("python"))) const;
            inline float y() __attribute__((annotate("python"))) const;
            inline float z() __attribute__((annotate("python"))) const;

        private:
            glm::vec3 m_data;
        };
    }
"""
    )

    result = util.GenerateOutput("templates/pyi_binding.j2")

    expected = """
        class Position:
            @overload
            def __init__(self, x: float, y: float, z: float,) -> None:
                ...

            @overload
            def __init__(self, other: "Position",) -> None:
                ...

            def x(self,) -> float:
                \"\"\"
                Method x is not documented
                \"\"\"
                ...

            def y(self,) -> float:
                \"\"\"
                Method y is not documented
                \"\"\"
                ...

            def z(self,) -> float:
                \"\"\"
                Method z is not documented
                \"\"\"
                ...
    """

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)


def test_not_binding_non_attribute_method_to_pyi(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
    namespace ntt {
        class __attribute__((annotate("python"))) Position {
        public:
            Position(float x, float y, float z) : m_data(x, y, z) {}
            Position(const Position &other) : m_data(other.m_data) {}
            ~Position() {}

            inline float x();
            inline float y() __attribute__((annotate("python"))) const;
            inline float z();

        private:
            glm::vec3 m_data;
        };
    }
    """
    )

    result = util.GenerateOutput("templates/pyi_binding.j2")

    expected = """
        class Position:
            @overload
            def __init__(self, x: float, y: float, z: float,) -> None:
                ...

            @overload
            def __init__(self, other: "Position",) -> None:
                ...

            def y(self,) -> float:
                \"\"\"
                Method y is not documented
                \"\"\"
                ...
    """

    assert util.ReformatOutput(expected) in util.ReformatOutput(result)
