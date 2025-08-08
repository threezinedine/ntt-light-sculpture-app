from dataclasses import dataclass, field
from .version import Version
from modules.dependency_injection.decorators import as_singleton


@as_singleton()
@dataclass
class Application:
    """
    Contain the all configure data for the current application. This data will be personalized
        for each user.
    """

    version: Version = field(default_factory=Version)
    recentProjectFilePaths: dict[str, str] = field(
        default_factory=dict
    )  # key: project name, value: project file path

    def Update(self, other: "Application") -> None:
        self.version.Update(other.version)
        self.recentProjectFilePaths = other.recentProjectFilePaths
