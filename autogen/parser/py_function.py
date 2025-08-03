from typing import List
import clang.cindex as clang  # type: ignore
from clang.cindex import Cursor  # type: ignore
from .py_argument import PyArgument


class PyFunction:
    def __init__(self, cursor: Cursor) -> None:
        self.name = cursor.spelling
        self.arguments: List[PyArgument] = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.PARM_DECL:
                self.arguments.append(PyArgument(child))

        self.return_type = cursor.result_type.spelling
        self.comment = self._get_comment(cursor)

    def _get_comment(self, cursor: Cursor) -> str:
        if cursor.brief_comment:
            return cursor.brief_comment
        else:
            return f"Function {self.name} is not documented"

    def __repr__(self) -> str:
        return f'<Method: name="{self.name}">'
