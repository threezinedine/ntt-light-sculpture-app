from dataclasses import dataclass, field
from .struct_base import StructBase


@dataclass
class OpenGLSetting(StructBase):
    drawEdges: bool = field(default=True)
    drawFaces: bool = field(default=True)

    def Update(self, other: StructBase) -> None:
        if not isinstance(other, OpenGLSetting):
            return

        self.drawEdges = other.drawEdges
        self.drawFaces = other.drawFaces

    def Compare(self, other: StructBase) -> bool:
        if not isinstance(other, OpenGLSetting):
            return False

        return self.drawEdges == other.drawEdges and self.drawFaces == other.drawFaces
