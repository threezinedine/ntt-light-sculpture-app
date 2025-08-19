from typing import List
import clang.cindex as clang  # type: ignore
from clang.cindex import Cursor  # type: ignore
from .py_method import PyMethod


class PyClass:
    def __init__(self, cursor: Cursor) -> None:
        self.name = cursor.spelling
        self.methods: List[PyMethod] = []
        self.annotations: List[str] = []
        self.hasDefaultConstructor = False
        self.constructors: List[PyMethod] = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.CXX_METHOD:
                if child.access_specifier == clang.AccessSpecifier.PUBLIC:
                    self.methods.append(PyMethod(child))
            elif child.kind == clang.CursorKind.CONSTRUCTOR:
                if child.access_specifier == clang.AccessSpecifier.PUBLIC:
                    self.hasDefaultConstructor |= child.is_default_constructor()
                    if not child.is_default_constructor():
                        self.constructors.append(PyMethod(child))
            elif child.kind == clang.CursorKind.ANNOTATE_ATTR:
                self.annotations.append(child.spelling)

    def __repr__(self) -> str:
        return f'<Class: name="{self.name}">'
