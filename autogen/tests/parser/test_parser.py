import pytest
from parser.py_method import PyMethod
from parser.py_attribute import PyAttribute
from parser.py_struct import PyStruct
from parser.py_argument import PyArgument
from parser.py_class import PyClass
from parser.py_function import PyFunction
from parser.parser import Parser


def assert_class(cls: PyClass, name: str) -> None:
    assert cls.name == name


def assert_method(
    method: PyMethod,
    name: str,
    isStatic: bool,
    returnType: str,
) -> None:
    assert method.name == name
    assert method.isStatic == isStatic
    assert method.returnType == returnType


def assert_function_arguments(
    argument: PyArgument,
    name: str,
    type: str,
) -> None:
    assert argument.name == name
    assert argument.type == type


def assert_function(
    function: PyFunction,
    name: str,
    returnType: str,
) -> None:
    assert function.name == name
    assert function.returnType == returnType


def assert_struct(struct: PyStruct, name: str) -> None:
    assert struct.name == name


def assert_attribute(attribute: PyAttribute, name: str, type: str) -> None:
    assert attribute.name == name
    assert attribute.type == type


@pytest.mark.skip(reason="Not implemented")
def test_parse_typedef() -> None:
    parser = Parser(
        "input.h",
        content="""
        namespace ntt 
        {
            typedef Function<void, const EngineLogRecord &> LogCallback;
        }
        """,
    )
    assert len(parser.data["types"]) == 1


def test_parse_class() -> None:
    parser = Parser(
        "input.h",
        content="""
        namespace ntt 
        {
            class Engine {
            public:
                void run() __attribute__((annotate("python")));
            protected:
                void run2() __attribute__((annotate("python")));
            private:
                void run3() __attribute__((annotate("python")));
            }
        }
        """,
    )

    assert len(parser.data["classes"]) == 1  # only public methods are parsed
    parsedClass: PyClass = parser.data["classes"][0]  # type: ignore
    assert parsedClass.name == "Engine"
    assert len(parsedClass.methods) == 1


def test_parse_function() -> None:
    parser = Parser(
        "input.h",
        content="""
        namespace ntt 
        {
            void run(int a, int b);
        }
        """,
    )

    assert len(parser.data["functions"]) == 1
    parsedFunction: PyFunction = parser.data["functions"][0]  # type: ignore

    assert_function(parsedFunction, "run", "void")
    assert_function_arguments(parsedFunction.arguments[0], "a", "int")
    assert_function_arguments(parsedFunction.arguments[1], "b", "int")


def test_parse_struct() -> None:
    parser = Parser(
        "input.h",
        content="""
        namespace ntt 
        {
            struct Engine {
                int a;
                int b;
            };
        }
        """,
    )

    assert len(parser.data["structs"]) == 1
    parsedStruct: PyStruct = parser.data["structs"][0]  # type: ignore
    assert_struct(parsedStruct, "Engine")
    assert_attribute(parsedStruct.attributes[0], "a", "int")
    assert_attribute(parsedStruct.attributes[1], "b", "int")


def test_does_not_parse_function_outside_namespace() -> None:
    parser = Parser(
        "input.h",
        content="""
        void run(int a, int b);
        """,
    )

    assert len(parser.data["functions"]) == 0


def test_parse_static_method_inside_class() -> None:
    parser = Parser(
        "input.h",
        content="""
        namespace ntt 
        {
            class Engine {
            public:
                void run();
                static void sRun();
            }
        }
        """,
    )

    assert len(parser.data["classes"]) == 1
    parsedClass: PyClass = parser.data["classes"][0]  # type: ignore
    assert_class(parsedClass, "Engine")

    assert len(parsedClass.methods) == 2
    assert_method(parsedClass.methods[0], "run", False, "void")
    assert_method(parsedClass.methods[1], "sRun", True, "void")
