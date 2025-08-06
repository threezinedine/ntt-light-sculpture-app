from dataclasses import dataclass, field


@dataclass
class Version:
    """
    Contain the version of the current application.
    """

    major: int = field(default=1)
    minor: int = field(default=0)
    patch: int = field(default=0)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
