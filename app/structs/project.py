from datetime import datetime
from dataclasses import dataclass

from .struct_base import StructBase


@dataclass
class Project(StructBase):
    """
    Contain all data of the current project. This data will be saved
        in the project file (.nlcp).

    All the information which related to the directory will be used as relative path.
    The project file will be saved in the directory of the project.
    """

    projectName: str
    createdAt: datetime
    lastEditAt: datetime

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, Project):
            raise ValueError("other is not a Project")

        self.projectName = other.projectName
        self.createdAt = other.createdAt
        self.lastEditAt = other.lastEditAt
