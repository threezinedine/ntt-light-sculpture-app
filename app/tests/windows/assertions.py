import os
from typing import Self
from pyfakefs.fake_filesystem import FakeFilesystem
from constants import TEST_NEW_PROJECT_PATH
from structs.application import Application
from structs.project import Project
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetProjectDataFile,
    GetProjectDataFolder,
)


class ProjectAssertion:
    def __init__(
        self,
        projectName: str,
        fs: FakeFilesystem | None = None,
    ) -> None:
        self._fs: FakeFilesystem | None = fs

        self._projectFolder = GetProjectDataFolder(TEST_NEW_PROJECT_PATH, projectName)
        self._projectFile = GetProjectDataFile(TEST_NEW_PROJECT_PATH, projectName)

        self._project: Project | None = None

        if os.path.exists(self._projectFile):
            with open(self._projectFile, "r") as f:
                self._project = Project()
                assert self._project.FromJson(f.read())

    def AssertProjectFolderDoesNotExist(self) -> Self:
        if self._fs is not None:
            assert not self._fs.exists(self._projectFolder)  # type: ignore
        return self

    def AssertProjectFileNotExists(self) -> Self:
        if self._fs is not None:
            assert not self._fs.exists(self._projectFile)  # type: ignore

        return self

    def AssertImages(self, imagePaths: list[str]) -> Self:
        assert self._project is not None

        for imagePath, inputImagePath in zip(self._project.imagePaths, imagePaths):
            assert imagePath == inputImagePath

        return self


class ApplicationAssertion:
    def __init__(self, fs: FakeFilesystem | None = None) -> None:
        self._fs = fs

        self._applicationDataFile = GetApplicationDataFile()

        self._application: Application | None = None

        if os.path.exists(self._applicationDataFile):
            with open(self._applicationDataFile, "r") as f:
                self._application = Application()
                assert self._application.FromJson(f.read())

    def AssertAppDataFolderDoesNotExist(self) -> Self:
        if self._fs is not None:
            assert not self._fs.exists(GetApplicationDataFolder())  # type: ignore
        return self

    def AssertRecentProjectsFileNotExists(self) -> Self:
        if self._fs is not None:
            assert not self._fs.exists(GetApplicationDataFile("recent_projects.json"))  # type: ignore
        return self

    def AssertRecentProjects(self, recentProjects: list[str]) -> Self:
        if self._fs is not None:
            assert self._fs.exists(GetApplicationDataFolder())  # type: ignore
            assert self._fs.exists(GetApplicationDataFile())  # type: ignore

        assert self._application is not None

        for recentProject, inputRecentProject in zip(
            self._application.recentProjectNames, recentProjects
        ):
            assert recentProject == inputRecentProject

        return self

    def Assert(self) -> Self:
        if self._fs is not None:
            assert self._fs.exists(GetApplicationDataFolder())  # type: ignore
            assert self._fs.exists(GetApplicationDataFile())  # type: ignore

        assert self._application is not None
        assert self._application.Compare(Application())

        return self
