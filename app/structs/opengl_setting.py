from copy import deepcopy
from dataclasses import dataclass, field

from utils.logger import logger  # type: ignore
from .struct_base import StructBase


@dataclass
class OpenGLSetting(StructBase):
    drawEdges: bool = field(default=True)
    drawFaces: bool = field(default=True)
    origin: list[float] = field(default_factory=lambda: [1, 1, 2])

    def Update(self, other: StructBase) -> None:
        if not isinstance(other, OpenGLSetting):
            return

        self.drawEdges = other.drawEdges
        self.drawFaces = other.drawFaces
        self.origin = deepcopy(other.origin)

    def Compare(self, other: StructBase) -> bool:
        if not isinstance(other, OpenGLSetting):
            return False

        return (
            self.drawEdges == other.drawEdges
            and self.drawFaces == other.drawFaces
            and self.origin == other.origin
        )

    def _Validate(self, loaded: StructBase) -> bool:
        if not isinstance(loaded, OpenGLSetting):
            return False

        if len(loaded.origin) != 3:
            return False

        return super()._Validate(loaded)
