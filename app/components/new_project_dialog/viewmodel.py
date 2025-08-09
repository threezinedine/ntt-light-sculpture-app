import os
from typing import Callable
from modules.dependency_injection.decorators import as_singleton
from structs.project import Project
from utils.application import GetProjectDataFolder


@as_singleton()
class NewProjectDialogViewModel:
    def __init__(self) -> None:
        self.project = Project()

        self._acceptCallback: Callable[[str, str], None] | None = None
        self._projectPath: str = ""
        self._projectName: str = ""

    def SetAcceptCallback(self, callback: Callable[[str, str], None] | None) -> None:
        self._acceptCallback = callback

    def Accept(self) -> None:
        if self._acceptCallback is None:
            return

        self._acceptCallback(self._projectPath, self._projectName)

    def Cancel(self) -> None:
        self._projectPath = ""
        self._projectName = ""

    @property
    def ProjectPath(self) -> str:
        return self._projectPath

    @ProjectPath.setter
    def ProjectPath(self, value: str) -> None:
        self._projectPath = value

    @property
    def ProjectName(self) -> str:
        return self._projectName

    @ProjectName.setter
    def ProjectName(self, value: str) -> None:
        self._projectName = value

    @property
    def FinalProjectPath(self) -> str:
        if self._projectPath == "" or self._projectName == "":
            return ""

        return GetProjectDataFolder(self._projectPath, self._projectName)

    @property
    def CanCreateProject(self) -> bool:
        return (
            self._projectPath != ""
            and self._projectName != ""
            and not os.path.exists(self.FinalProjectPath)
        )
