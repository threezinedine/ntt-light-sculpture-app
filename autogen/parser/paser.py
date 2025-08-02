import os
import clang.cindex as clang
from clang.cindex import Config
from .method import Method


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
        self._ast = index.parse(input_file, args=["-x", "c++"])

        for c in self._ast.cursor.get_children():
            if c.kind == clang.CursorKind.NAMESPACE:
                for child in c.get_children():
                    if child.kind == clang.CursorKind.FUNCTION_DECL:
                        print(Method(child))

    def parse(self) -> None:
        pass
