import clang.cindex as clang  # type: ignore


class PyTypedef:
    def __init__(self, cursor: clang.Cursor) -> None:
        self.name = cursor.spelling

    def __repr__(self) -> str:
        return f'<PyTypedef name="{self.name}" />'
