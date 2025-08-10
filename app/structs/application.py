from dataclasses import dataclass, field
from copy import deepcopy

from constants import MAX_NUMBER_OF_RECENT_PROJECTS

from .struct_base import StructBase
from .version import Version


@dataclass
class Application(StructBase):
    """
    Contain the all configure data for the current application. This data will be personalized
        for each user.
    """

    version: Version = field(default_factory=Version)
    recentProjectNames: list[str] = field(default_factory=list)
    recentProjectFilePaths: dict[str, str] = field(default_factory=dict)

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, Application):
            raise ValueError("other is not a Application")

        self.version.Update(other.version)
        self.recentProjectFilePaths = deepcopy(other.recentProjectFilePaths)
        self.recentProjectNames = deepcopy(other.recentProjectNames)

    def Compare(self, other: "StructBase") -> bool:
        if not isinstance(other, Application):
            raise ValueError("other is not a Application")

        if not self.version.Compare(other.version):
            return False

        for projectName in self.recentProjectNames:
            if projectName not in other.recentProjectNames:
                return False

        return True

    def _Validate(self, loaded: "StructBase") -> bool:
        if not isinstance(loaded, Application):
            return False

        if len(loaded.recentProjectNames) > MAX_NUMBER_OF_RECENT_PROJECTS:
            removedProjectNames = loaded.recentProjectNames[
                MAX_NUMBER_OF_RECENT_PROJECTS:
            ]

            for projectName in removedProjectNames:
                del loaded.recentProjectFilePaths[projectName]

            loaded.recentProjectNames = loaded.recentProjectNames[
                :MAX_NUMBER_OF_RECENT_PROJECTS
            ]

        for projectName in loaded.recentProjectNames:
            if projectName not in loaded.recentProjectFilePaths:
                return False

        return True
