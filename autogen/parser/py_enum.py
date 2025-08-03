import clang.cindex as clang  # type: ignore
from typing import List


class PyEnumConstant:
    def __init__(self, cursor: clang.Cursor) -> None:
        self.name = cursor.spelling
        self.value = cursor.enum_value

    def __repr__(self) -> str:
        return f"<PyEnumConstant name={self.name} value={self.value} />"


class PyEnum:
    def __init__(self, cursor: clang.Cursor) -> None:
        self.name = cursor.spelling
        self.constants: List[PyEnumConstant] = []
        self.comment = cursor.brief_comment

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.ENUM_CONSTANT_DECL:
                self.constants.append(PyEnumConstant(child))

    def __repr__(self) -> str:
        return f"<PyEnum name={self.name} constants={self.constants} />"
