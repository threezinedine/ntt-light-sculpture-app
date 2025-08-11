import cv2 as cv
from modules.dependency_injection.helper import as_dependency
from structs.application import Application
from structs.project import Project
from utils.application import GetImageFilePath
from PIL import Image
import numpy as np


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
        if self._index < 0 or self._index >= len(self._project.images):
            return None

        imagePath = GetImageFilePath(
            self._application.CurrentProjectDirectory, self._project.images[self._index]
        )

        finalImage = Image.open(imagePath)

        return cv.cvtColor(np.array(finalImage), cv.COLOR_RGB2BGR)  # type: ignore
