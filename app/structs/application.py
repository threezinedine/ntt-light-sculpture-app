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
    recentProjectFilePaths: dict[str, str] = field(
        default_factory=dict
    )  # key: project name, value: project file path

    def Update(self, other: "StructBase") -> None:
        if not isinstance(other, Application):
            raise ValueError("other is not a Application")

        self.version.Update(other.version)
        self.recentProjectFilePaths = other.recentProjectFilePaths
