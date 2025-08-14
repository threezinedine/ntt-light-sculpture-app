from typing import Any
from modules.history_manager import Command
from structs.image_meta import ImageMeta


class ChangeThesholdCommand(Command):
    def __init__(self, metaFile: ImageMeta, preValue: int):
        self._metaFile = metaFile
        self._preValue = preValue

    def _ExecuteImpl(self, *args: Any, **kwargs: Any) -> None:
        pass

    def _UndoImpl(self) -> None:
        self._metaFile.threshold = self._preValue
