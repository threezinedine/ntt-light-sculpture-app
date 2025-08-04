import os
import clang.cindex as clang  # type: ignore
from clang.cindex import Config  # type: ignore
from typing import Dict, List, Optional, Union, Literal

from .py_function import PyFunction
from .py_class import PyClass
from .py_enum import PyEnum
from .py_struct import PyStruct

ParserDataKey = Literal["types", "enums", "structs", "classes", "functions"]
ParserDataType = Union[PyFunction, PyClass, PyEnum, PyStruct]


class Parser:
    """
    The parser will read the input file and parse them into a predefined data structure
        inside this project, after that, user can use the jinja template for rendering
        the generated source code.

    Parameters:
        inputFile: The file to parse, this file will be parsed by clang, all #include will be
                    solved by the clang.
        content: This attribute is used for testing only, do not used it for other purposes. If
                    this attribute is not None, then the inputFile will not be searched in the
                    real file system, instead, the content will be used as the input file.

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
    def ConfigClang(libClangDllPath: str) -> None:
        """
        Must be called before creating the parser.

        Parameters:
            libClangDllPath: The absolute path of the libclang.dll which will be
                loaded into the current project for parsing the .h files.

        Example:
        ```python
        Parser.ConfigClang("libclang.dll")
        ```
        """
        Config.set_library_file(libClangDllPath)

    def __init__(self, inputFile: str, content: Optional[str] = None) -> None:
        if content is None:
            if not os.path.exists(inputFile):
                raise FileNotFoundError(f"Input file '{inputFile}' does not exist")

        index = clang.Index.create()
        self._ast = index.parse(  # type: ignore
            inputFile,
            args=[
                "-x",
                "c++",
                "-std=c++17",
                "-fgnu-extensions",
                "-fparse-all-comments",
            ],
            unsaved_files=[(inputFile, content)] if content else None,
        )
        self._data: Dict[ParserDataKey, List[ParserDataType]] = {
            "types": [],
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
    def data(self) -> Dict[ParserDataKey, List[ParserDataType]]:
        return self._data
