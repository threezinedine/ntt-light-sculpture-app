import os
from typing import Self
from PyQt6.QtWidgets import QTabWidget
from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from constants import TEST_NEW_PROJECT_PATH
from structs.application import Application
from structs.image_meta import ImageMeta
from structs.project import Project
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetImageFilePath,
    GetProjectDataFile,
    GetProjectDataFolder,
    GetTestProjectDataFolder,
)
from utils.logger import logger  # type: ignore
from abc import ABC, abstractmethod


class Assertable(ABC):
    """
    Just the constructed form for all assertions
    """

    @abstractmethod
    def Assert(self) -> None:
        """
        Only run assertions in this method, other method should be used for storing the
            information for this assertion operation.

        Args:
            fs (FakeFilesystem | None): The fake filesystem to use for assertions, this
                value can be None.
        """
        pass


class ProjectAssertion(Assertable):
    def __init__(
        self,
        projectName: str,
    ) -> None:
        self._projectFolder = GetProjectDataFolder(TEST_NEW_PROJECT_PATH, projectName)
        self._projectFile = GetProjectDataFile(TEST_NEW_PROJECT_PATH, projectName)

        self.project: Project | None = None
        self._shouldProjectFolderExisted = True
        self._shouldProjectFileExisted = True
        self._expectedImagesCount: int | None = None

        self._images: list[ImageAssertion] = []

        if os.path.exists(self._projectFile):
            with open(self._projectFile, "r") as f:
                self.project = Project()
                assert self.project.FromJson(f.read())

    def AssertProjectFolderDoesNotExist(self) -> Self:
        self._shouldProjectFolderExisted = False
        return self

    def AssertProjectFileNotExists(self) -> Self:
        self._shouldProjectFileExisted = False
        return self

    def AssertImage(self, image: "ImageAssertion") -> Self:
        image.SetOwnerProject(self)
        self._images.append(image)
        return self

    def AssertImagesCount(self, imageCount: int) -> Self:
        self._expectedImagesCount = imageCount
        return self

    def Assert(self) -> None:
        if not self._shouldProjectFolderExisted:
            assert not os.path.exists(
                self._projectFolder
            ), f"Project folder {self._projectFolder} should not exist"
            return

        if not self._shouldProjectFileExisted:
            assert not os.path.exists(
                self._projectFile
            ), f"Project file {self._projectFile} should not exist"

        assert self.project is not None

        if self._expectedImagesCount is not None:
            assert (
                len(self._images) == self._expectedImagesCount
            ), f"Expected {self._expectedImagesCount} images but got {len(self._images)}"

        for image in self._images:
            image.Assert()


class ApplicationAssertion(Assertable):
    def __init__(self) -> None:
        self._applicationDataFile = GetApplicationDataFile()

        self._application: Application | None = None
        self._shouldAppDataFolderExisted = True
        self._shouldAppDataFileExisted = True

        self._recentProjectNames: list[str] = []
        self._projects: list[ProjectAssertion] = []

        if os.path.exists(self._applicationDataFile):
            with open(self._applicationDataFile, "r") as f:
                self._application = Application()
                assert self._application.FromJson(f.read())

    def AssertAppDataFolderDoesNotExist(self) -> Self:
        self._shouldAppDataFolderExisted = False
        return self

    def AssertRecentProjectsFileNotExists(self) -> Self:
        self._shouldAppDataFileExisted = False
        return self

    def AssertRecentProjects(self, recentProjects: list[str]) -> Self:
        self._recentProjectNames = recentProjects

        return self

    def AssertProject(self, project: ProjectAssertion) -> Self:
        self._projects.append(project)
        return self

    def Assert(self) -> None:
        if not self._shouldAppDataFolderExisted:
            assert not os.path.exists(
                GetApplicationDataFolder()
            ), f"Application data folder {GetApplicationDataFolder()} should not exist"

        if not self._shouldAppDataFileExisted:
            assert not os.path.exists(
                GetApplicationDataFile()
            ), f"Application data file {GetApplicationDataFile()} should not exist"

        assert self._application is not None, "Application data is not loaded"

        assert set(self._recentProjectNames) == set(
            self._application.recentProjectNames
        ), f"Recent projects do not match: {self._recentProjectNames} != {self._application.recentProjectNames}"

        for project in self._projects:
            project.Assert()


class TabWidgetAssertion:
    def __init__(self, tabWidget: QTabWidget) -> None:
        self._tabWidget = tabWidget

    def AssertCurrentTabName(self, name: str) -> Self:
        index = self._tabWidget.currentIndex()
        assert self._tabWidget.tabText(index) == name
        return self

    def AssertTabCount(self, count: int) -> Self:
        assert self._tabWidget.count() == count
        return self

    def AssertImagePreviewWidgetNotEmpty(self, index: int) -> Self:
        assert self._tabWidget.widget(index) is not None

        imagePreviewWidget: ImagePreviewWidget = self._tabWidget.widget(index)  # type: ignore

        assert imagePreviewWidget.ui.imagePreviewLabel.hasContent
        assert imagePreviewWidget.ui.binaryImageLabel.hasContent
        return self


class ImageAssertion(Assertable):
    def __init__(self, imageName: str) -> None:
        super().__init__()
        self._ownerProjectAssertion: ProjectAssertion | None = None
        self._imageName = imageName
        self._imageBeCopied = True
        self._expectedThreshold: int | None = None

    def SetOwnerProject(self, project: ProjectAssertion) -> None:
        self._ownerProjectAssertion = project

    def AssertImageNotBeCopied(self) -> Self:
        self._imageBeCopied = False
        return self

    def AssertThreshold(self, threshold: int) -> Self:
        self._expectedThreshold = threshold
        return self

    def Assert(self) -> None:
        assert (
            self._ownerProjectAssertion is not None
        ), "Owner project assertion is not set"

        assert self._ownerProjectAssertion.project is not None, "Project is not loaded"

        project = self._ownerProjectAssertion.project
        imageData: ImageMeta | None = None

        for image in project.images:
            if image.name == self._imageName:
                imageData = image
                break

        assert imageData is not None, "Image data is not found"

        projectFolder = GetTestProjectDataFolder(project.projectName)
        copiedImagePath = GetImageFilePath(projectFolder, self._imageName)
        if not self._imageBeCopied:
            assert not os.path.exists(
                copiedImagePath
            ), f"Image file {copiedImagePath} should not exist"
        else:
            assert os.path.exists(
                copiedImagePath
            ), f"Image file {copiedImagePath} should exist"

        if self._expectedThreshold is not None:
            assert (
                imageData.threshold == self._expectedThreshold
            ), f"Expected {self._expectedThreshold} but got {imageData.threshold}"
