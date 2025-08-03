from typing import List
import clang.cindex as clang  # type: ignore
from .py_attribute import PyAttribute


class PyStruct:
    def __init__(self, cursor: clang.Cursor):
        self.name = cursor.spelling
        self.attributes: List[PyAttribute] = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.FIELD_DECL:
                self.attributes.append(PyAttribute(child))

    def __repr__(self):
        return f"<Struct name={self.name} />"
