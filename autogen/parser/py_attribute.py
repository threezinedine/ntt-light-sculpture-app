import clang.cindex as clang  # type: ignore


class PyAttribute:
    def __init__(self, cursor: clang.Cursor) -> None:
        self.name = cursor.spelling
        self.type = cursor.type.spelling
        self.comment = cursor.brief_comment

    def __repr__(self) -> str:
        return f"<PyAttribute name={self.name} type={self.type} />"
