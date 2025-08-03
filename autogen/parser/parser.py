import os
import clang.cindex as clang  # type: ignore
from clang.cindex import Config  # type: ignore
from typing import Dict, List, Union

from .py_function import PyFunction
from .py_class import PyClass
from .py_enum import PyEnum
from .py_struct import PyStruct

ParserDataType = Union[PyFunction, PyClass, PyEnum, PyStruct]

class Parser:
    """
    The parser will read the input file and parse them into a predefined data structure
        inside this project, after that, user can use the jinja template for rendering
        the generated source code.

    Example:
    ```cpp
    class Engine
    {
    public:
        void run() __attribute__((annotate("python")));
    };
    ```

    ```python
    Parser.ConfigClang("libclang.dll")
    parser = Parser("input.h")
    data = parser.parse()
    ```

    so that the `data` will has the following structure (not the exact structure, just an example):
    ```python
    {
        "classes": [
            {
                "name": "Engine",
                "functions": [
                    {"name": "run", "type": "void", "attributes": ["python"]}
                ]
            }
        ]
    }
    """

    @staticmethod
    def ConfigClang(libclang_path: str) -> None:
        """
        Must be called before creating the parser.
        """
        Config.set_library_file(libclang_path)

    def __init__(self, input_file: str) -> None:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' does not exist")

        index = clang.Index.create()
        self._ast = index.parse(input_file, args=["-x", "c++"])  # type: ignore
        self._data: Dict[str, List[ParserDataType]] = {
            "enums": [],
            "structs": [],
            "classes": [],
            "functions": [],
        }

        for c in self._ast.cursor.get_children():  # type: ignore
            if c.kind == clang.CursorKind.NAMESPACE and c.spelling == "ntt":
                for child in c.get_children():
                    if child.kind == clang.CursorKind.FUNCTION_DECL:
                        function = PyFunction(child)
                        self.data["functions"].append(function)
                    elif child.kind == clang.CursorKind.CLASS_DECL:
                        class_ = PyClass(child)
                        self.data["classes"].append(class_)
                    elif child.kind == clang.CursorKind.ENUM_DECL:
                        enum = PyEnum(child)
                        self.data["enums"].append(enum)
                    elif child.kind == clang.CursorKind.STRUCT_DECL:
                        struct = PyStruct(child)
                        self.data["structs"].append(struct)

    @property
    def data(self) -> Dict[str, List[ParserDataType]]:
        return self._data
