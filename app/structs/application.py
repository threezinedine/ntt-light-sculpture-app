from dataclasses import dataclass, field

from .struct_base import StructBase
from .version import Version
from modules.dependency_injection.decorators import as_singleton


@as_singleton()
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
        self.recentProjectFilePaths = other.recentProjectFilePaths

    def Compare(self, other: "StructBase") -> bool:
        if not isinstance(other, Application):
            raise ValueError("other is not a Application")

        if not self.version.Compare(other.version):
            return False

        for projectName in self.recentProjectNames:
            if projectName not in other.recentProjectNames:
                return False

        return True

    def _Valide(self, loaded: "StructBase") -> bool:
        if not isinstance(loaded, Application):
            return False

        for projectName in loaded.recentProjectNames:
            if projectName not in loaded.recentProjectFilePaths:
                return False

        return True
