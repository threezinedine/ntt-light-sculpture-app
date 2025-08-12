import os
from typing import Self
from PyQt6.QtWidgets import QTabWidget
from pyfakefs.fake_filesystem import FakeFilesystem
from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from constants import TEST_NEW_PROJECT_PATH
from structs.application import Application
from structs.image_meta import ImageMeta
from structs.project import Project
from utils.application import (
    GetApplicationDataFile,
    GetApplicationDataFolder,
    GetImageFilePath,
    GetImageMetadataFile,
    GetProjectDataFile,
    GetProjectDataFolder,
    GetTestProjectDataFolder,
)
from utils.logger import logger  # type: ignore


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

    def AssertImages(self, images: list[str]) -> Self:
        assert self._project is not None

        for image, inputImage in zip(self._project.images, images):
            assert image == inputImage

        return self

    def AssertImageLoadded(self) -> Self:
        assert self._fs is not None
        assert self._project is not None

        for image in self._project.images:
            loadedImagePath = GetImageFilePath(
                os.path.join(TEST_NEW_PROJECT_PATH, self._project.projectName),
                image,
            )

            assert self._fs.exists(loadedImagePath), f"Image {loadedImagePath} is not loaded"  # type: ignore

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

    def AssertRecentProjectFilePaths(self) -> Self:
        assert self._application is not None

        for projectName in self._application.recentProjectNames:
            dataFile = GetProjectDataFile(TEST_NEW_PROJECT_PATH, projectName)
            assert self._fs.exists(dataFile)  # type: ignore

            assert self._application.recentProjectFilePaths[projectName] == dataFile

        return self

    def Assert(self) -> Self:
        if self._fs is not None:
            assert self._fs.exists(GetApplicationDataFolder())  # type: ignore
            assert self._fs.exists(GetApplicationDataFile())  # type: ignore

        assert self._application is not None
        assert self._application.Compare(Application())

        return self


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


class ImageMetadataAssertion:
    def __init__(
        self,
        projectName: str,
        imageName: str,
        fs: FakeFilesystem | None = None,
    ) -> None:
        self._fs = fs

        self._metadataFile = GetImageMetadataFile(
            GetTestProjectDataFolder(projectName), imageName
        )
        logger.debug(f"metadataFile: {self._metadataFile}")
        self._metadata: ImageMeta | None = None

        if os.path.exists(self._metadataFile):
            with open(self._metadataFile, "r") as f:
                self._metadata = ImageMeta()
                assert self._metadata.FromJson(f.read())

    def AssertMetadataFileNotExists(self) -> Self:
        assert not os.path.exists(self._metadataFile)

        return self

    def AssertFileExists(self) -> Self:
        logger.debug(f"metadataFile: {self._metadataFile}")
        assert os.path.exists(self._metadataFile)
        return self

    def AssertThreshold(self, threshold: int) -> Self:
        assert self._metadata is not None, "Metadata is not loaded"

        assert (
            self._metadata.threshold == threshold
        ), f"Expected {threshold} but got {self._metadata.threshold}"

        return self
