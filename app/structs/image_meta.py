from dataclasses import dataclass, field
from datetime import datetime

from .struct_base import StructBase


@dataclass
class ImageMeta(StructBase):
    copiedAt: float = field(default=datetime.now().timestamp())
    threshold: int = field(default=128)

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, ImageMeta):
            raise ValueError("other is not a ImageMeta")

        self.copiedAt = other.copiedAt
        self.threshold = other.threshold

    def Compare(self, other: "StructBase") -> bool:
        if not isinstance(other, ImageMeta):
            raise ValueError("other is not a ImageMeta")

        return self.copiedAt == other.copiedAt and self.threshold == other.threshold

    def _Validate(self, loaded: "StructBase") -> bool:
        if not isinstance(loaded, ImageMeta):
            raise ValueError("loaded is not a ImageMeta")

        if loaded.threshold < 0:
            loaded.threshold = 0
        if loaded.threshold > 255:
            loaded.threshold = 255

        return super()._Validate(loaded)
