import clang.cindex as clang
from .argument import Argument


class Method:
    def __init__(self, cursor: clang.Cursor):
        self.name = cursor.spelling
        self.arguments = []

        for child in cursor.get_children():
            if child.kind == clang.CursorKind.PARM_DECL:
                self.arguments.append(Argument(child))

        self.return_type = cursor.result_type.spelling
        self.comment = self._get_comment(cursor)

    def _get_comment(self, cursor: clang.Cursor) -> str:
        if cursor.brief_comment:
            return cursor.brief_comment
        else:
            return f"Method {self.name} is not documented"

    def __repr__(self) -> str:
        return f'<Method: name="{self.name}">'
