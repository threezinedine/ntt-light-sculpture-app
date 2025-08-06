from dataclasses import dataclass
from .version import Version


@dataclass
class Application:
    """
    Contain the all configure data for the current application. This data will be personalized
        for each user.
    """

    version: Version
    recentProjectFilePaths: dict[
        str, str
    ]  # key: project name, value: project file path
