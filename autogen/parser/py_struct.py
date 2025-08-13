from typing import List
import clang.cindex as clang  # type: ignore

from parser.py_method import PyMethod
from .py_attribute import PyAttribute


class PyStruct:
    def __init__(self, cursor: clang.Cursor):
        self.name = cursor.spelling
        self.comment = cursor.brief_comment
        self.attributes: List[PyAttribute] = []
        self.methods: List[PyMethod] = []
        self.constructors: List[PyMethod] = []
        self.hasDefaultConstructor = False
        self._constructorCount: int = 0
        self.annotations: List[str] = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.FIELD_DECL:
                self.attributes.append(PyAttribute(child))
            elif child.kind == clang.CursorKind.CONSTRUCTOR:
                self._constructorCount += 1
                if child.is_default_constructor():
                    self.hasDefaultConstructor = True
                else:
                    self.constructors.append(PyMethod(child))
            elif child.kind == clang.CursorKind.CXX_METHOD:
                self.methods.append(PyMethod(child))
            elif child.kind == clang.CursorKind.ANNOTATE_ATTR:
                self.annotations.extend(child.spelling.split(","))

        if self._constructorCount == 0:
            self.hasDefaultConstructor = True

    def __repr__(self):
        return f"<Struct name={self.name} />"
