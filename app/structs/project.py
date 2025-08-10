from datetime import datetime
from dataclasses import dataclass, field

from .struct_base import StructBase


@dataclass
class Project(StructBase):
    """
    Contain all data of the current project. This data will be saved
        in the project file (.nlcp).

    All the information which related to the directory will be used as relative path.
    The project file will be saved in the directory of the project.
    """

    projectName: str = field(default="")
    createdAt: int = field(default=0)
    lastEditAt: int = field(default=0)

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, Project):
            raise ValueError("other is not a Project")

        self.projectName = other.projectName
        self.createdAt = other.createdAt
        self.lastEditAt = other.lastEditAt

    def Compare(self, other: "StructBase") -> bool:
        if not isinstance(other, Project):
            raise ValueError("other is not a Project")

        if self.projectName != other.projectName:
            return False

        return True

    def GetCreatedAt(self) -> datetime:
        return datetime.fromtimestamp(self.createdAt)

    def GetLastEditAt(self) -> datetime:
        return datetime.fromtimestamp(self.lastEditAt)

    def SetCreatedAt(self, createdAt: datetime) -> None:
        self.createdAt = int(createdAt.timestamp())

    def SetLastEditAt(self, lastEditAt: datetime) -> None:
        self.lastEditAt = int(lastEditAt.timestamp())
