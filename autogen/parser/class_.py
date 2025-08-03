from typing import List, Union
import clang.cindex as clang  # type: ignore
from clang.cindex import Cursor  # type: ignore
from .method import Method


class Class:
    def __init__(self, cursor: Cursor) -> None:
        self.name = cursor.spelling

        self.methods: List[Union[Method, Class]] = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.CXX_METHOD:
                if child.access_specifier == clang.AccessSpecifier.PUBLIC:
                    self.methods.append(Method(child))

    def __repr__(self) -> str:
        return f'<Class: name="{self.name}">'
