from dataclasses import dataclass


@dataclass
class Version:
    """
    Contain the version of the current application.
    """

    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
