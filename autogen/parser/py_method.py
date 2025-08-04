from typing import List, Optional
import clang.cindex as clang  # type: ignore
from .py_argument import PyArgument


class PyMethod:
    def __init__(
        self,
        cursor: clang.Cursor,
    ):
        self.name = cursor.spelling
        self.arguments: List[PyArgument] = []
        self.annotation: Optional[str] = None

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.PARM_DECL:
                self.arguments.append(PyArgument(child))
            elif child.kind == clang.CursorKind.ANNOTATE_ATTR:
                self.annotation = child.spelling

        self.returnType = cursor.result_type.spelling
        self.isStatic: bool = cursor.is_static_method()
        self.comment = self._get_comment(cursor)

    def _get_comment(self, cursor: clang.Cursor) -> str:
        if cursor.brief_comment:
            return cursor.brief_comment
        else:
            return f"Method {self.name} is not documented"

    def __repr__(self) -> str:
        return f'<Method: name="{self.name}">'
