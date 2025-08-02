from clang.cindex import Cursor


class Method:
    def __init__(self, cursor: Cursor) -> None:
        self.name = cursor.spelling

    def __repr__(self) -> str:
        return f'<Method: name="{self.name}">'
