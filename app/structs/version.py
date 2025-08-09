from dataclasses import dataclass, field

from .struct_base import StructBase


@dataclass
class Version(StructBase):
    """
    Contain the version of the current application.
    """

    major: int = field(default=1)
    minor: int = field(default=0)
    patch: int = field(default=0)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, Version):
            raise ValueError("other is not a Version")

        self.major = other.major
        self.minor = other.minor
        self.patch = other.patch
