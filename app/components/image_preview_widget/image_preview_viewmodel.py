import cv2 as cv
from modules.dependency_injection.helper import as_dependency
from structs.application import Application
from structs.project import Project
from utils.application import GetImageFilePath
from utils.images import ConvertToBinary, LoadImage


@as_dependency(Project, Application)
class ImagePreviewViewModel:
    def __init__(
        self,
        project: Project,
        application: Application,
    ):
        self._index = 0
        self._project = project
        self._application = application

        self._isLoaded = False
        self._image: cv.Mat | None = None

    @property
    def Index(self) -> int:
        return self._index

    @Index.setter
    def Index(self, value: int) -> None:
        self._index = value

    @property
    def TabName(self) -> str:
        if self._index < 0 or self._index >= len(self._project.images):
            return ""
        return self._project.images[self._index]

    @property
    def Image(self) -> cv.Mat | None:
        if self._isLoaded:
            return self._image

        if self._index < 0 or self._index >= len(self._project.images):
            return None

        imagePath = GetImageFilePath(
            self._application.CurrentProjectDirectory, self._project.images[self._index]
        )

        self._image = LoadImage(imagePath)
        self._isLoaded = True
        return self._image

    @property
    def BinaryImage(self) -> cv.Mat | None:
        if self._index < 0 or self._index >= len(self._project.images):
            return None

        return ConvertToBinary(self._image)
