import cv2 as cv
from modules.dependency_injection.helper import as_dependency
from structs.application import Application
from structs.image_meta import ImageMeta
from structs.project import Project
from utils.application import GetImageFilePath
from utils.images import ConvertToBinary, LoadImage
from utils.logger import logger  # type: ignore


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
        self._metaFile: ImageMeta | None = None

        self._isLoaded = False
        self._image: cv.Mat | None = None

    @property
    def Index(self) -> int:
        return self._index

    @Index.setter
    def Index(self, value: int) -> None:
        self._metaFile = self._project.images[value]
        self._index = value

    @property
    def TabName(self) -> str:
        if self._index < 0 or self._index >= len(self._project.images):
            return ""
        return self._project.images[self._index].name

    @property
    def Threshold(self) -> int:
        if self._metaFile is None:
            return 0

        return self._metaFile.threshold

    @Threshold.setter
    def Threshold(self, value: int) -> None:
        if self._metaFile is None:
            return

        self._metaFile.threshold = value

    @property
    def Image(self) -> cv.Mat | None:
        if self._isLoaded:
            return self._image

        if self._index < 0 or self._index >= len(self._project.images):
            return None

        imagePath = GetImageFilePath(
            self._application.CurrentProjectDirectory,
            self._project.images[self._index].name,
        )

        self._image = LoadImage(imagePath)
        self._isLoaded = True
        return self._image

    def GetBinaryImage(self, threshold: int) -> cv.Mat | None:
        if self.Image is None:
            return None

        return ConvertToBinary(self.Image, threshold)
