from datetime import datetime
from dataclasses import dataclass


@dataclass
class Project:
    """
    Contain all data of the current project. This data will be saved
        in the project file (.nlcp).

    All the information which related to the directory will be used as relative path.
    The project file will be saved in the directory of the project.
    """

    projectName: str
    createdAt: datetime
    lastEditAt: datetime
