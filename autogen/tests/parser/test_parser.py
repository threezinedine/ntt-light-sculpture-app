from typing import List, Optional
import pytest  # type: ignore
from parser.py_method import PyMethod
from parser.py_attribute import PyAttribute
from parser.py_struct import PyStruct
from parser.py_argument import PyArgument
from parser.py_class import PyClass
from parser.py_function import PyFunction
from parser.py_typedef import PyTypedef
from conftest import AutoGenUtil


def assert_class(
    cls: PyClass,
    name: str,
    annotations: Optional[List[str]] = None,
) -> None:
    assert cls.name == name

    if annotations is not None:
        for annotation in annotations:
            assert annotation in cls.annotations


def assert_method(
    method: PyMethod,
    name: str,
    isStatic: bool,
    returnType: str,
    annotations: Optional[List[str]] = None,
) -> None:
    assert method.name == name
    assert method.isStatic == isStatic
    assert method.returnType == returnType

    if annotations is not None:
        for annotation in annotations:
            assert annotation in method.annotations


def assert_arguments(
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


def assert_struct(
    struct: PyStruct, name: str, hasDefaultConstructor: bool = True
) -> None:
    assert struct.name == name
    assert struct.hasDefaultConstructor == hasDefaultConstructor


def assert_attribute(attribute: PyAttribute, name: str, type: str) -> None:
    assert attribute.name == name
    assert attribute.type == type


def assert_typedef(typedef: PyTypedef, name: str) -> None:
    assert typedef.name == name


def test_parse_typedef(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        #include <functional>

        template <typename T, typename... Args>
        using Function = std::function<T(Args...)>;

        namespace ntt 
        {
            typedef Function<void, const EngineLogRecord &> LogCallback;
        }
        """,
    )
    parsedData = util.GetParsedData()
    assert len(parsedData["typedefs"]) == 1
    parsedTypedef: PyTypedef = parsedData["typedefs"][0]  # type: ignore
    assert_typedef(parsedTypedef, "LogCallback")


def test_parse_class(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
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

    parsedData = util.GetParsedData()
    assert len(parsedData["classes"]) == 1  # only public methods are parsed
    parsedClass: PyClass = parsedData["classes"][0]  # type: ignore
    assert parsedClass.name == "Engine"
    assert len(parsedClass.methods) == 1


def test_parse_function(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            void run(int a, int b);
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["functions"]) == 1
    parsedFunction: PyFunction = parsedData["functions"][0]  # type: ignore

    assert_function(parsedFunction, "run", "void")
    assert_arguments(parsedFunction.arguments[0], "a", "int")
    assert_arguments(parsedFunction.arguments[1], "b", "int")


def test_parse_struct(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            struct Engine {
                int a;
                int b;
            };
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["structs"]) == 1
    parsedStruct: PyStruct = parsedData["structs"][0]  # type: ignore
    assert_struct(parsedStruct, "Engine")
    assert_attribute(parsedStruct.attributes[0], "a", "int")
    assert_attribute(parsedStruct.attributes[1], "b", "int")


def test_does_not_parse_function_outside_namespace(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        void run(int a, int b);
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["functions"]) == 0


def test_parse_static_method_inside_class(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            struct Data 
            {
                int a;
                int b;
            };

            class Engine 
            {
            public:
                void run(const Data &data) __attribute__((annotate("python")));
                static void sRun() __attribute__((annotate("python")));
            }
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["classes"]) == 1
    parsedClass: PyClass = parsedData["classes"][0]  # type: ignore
    assert_class(parsedClass, "Engine")

    assert len(parsedClass.methods) == 2
    assert_method(parsedClass.methods[0], "run", False, "void", ["python"])
    assert len(parsedClass.methods[0].arguments) == 1
    assert_arguments(parsedClass.methods[0].arguments[0], "data", "const Data &")
    assert_method(parsedClass.methods[1], "sRun", True, "void", ["python"])


def test_parse_singleton_class(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            class __attribute__((annotate("singleton"))) Engine 
            {
            public:
                void run() __attribute__((annotate("python")));
            };
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["classes"]) == 1
    parsedClass: PyClass = parsedData["classes"][0]  # type: ignore
    assert_class(parsedClass, "Engine", ["singleton"])

    assert len(parsedClass.methods) == 1
    assert_method(parsedClass.methods[0], "run", False, "void", ["python"])


def test_parse_struct_with(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            struct Engine {
                int a;
                int b;
            };
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["structs"]) == 1
    parsedStruct: PyStruct = parsedData["structs"][0]  # type: ignore
    assert_struct(parsedStruct, "Engine")


def test_parse_struct_without_default_constructor(util: AutoGenUtil) -> None:
    util.CreateInputFile(
        """
        namespace ntt 
        {
            struct Engine {
                int a;
                int b;

                Engine(int a, int b) : a(a), b(b) {}
            };
        }
        """,
    )

    parsedData = util.GetParsedData()
    assert len(parsedData["structs"]) == 1
    parsedStruct: PyStruct = parsedData["structs"][0]  # type: ignore
    assert_struct(parsedStruct, "Engine", False)
