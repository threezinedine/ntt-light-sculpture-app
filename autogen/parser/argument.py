from clang.cindex import Cursor


class Argument:
    def __init__(self, cursor: Cursor) -> None:
        self.name = cursor.spelling
        self.type = cursor.type.spelling

    def __repr__(self) -> str:
        return f'<Argument: name="{self.name}" type="{self.type}">'
