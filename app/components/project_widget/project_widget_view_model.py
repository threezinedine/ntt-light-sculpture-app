import shutil
from PyQt6.QtGui import QStandardItem
from constants import MODIFY_IMAGES_LIST_EVENT_NAME
from structs.application import Application
from structs.image_meta import ImageMeta
from structs.project import Project
from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from utils.application import (
    GetImageFileNameFromFilePath,
    GetImageFilePath,
    GetImageMetadataFile,
    GetImageNameBasedOnExistedImageNames,
)
from utils.logger import logger  # type: ignore


class ImageItem(QStandardItem):
    def __init__(
        self,
        imagePath: str,
    ) -> None:
        super().__init__()
        self.imagePath = imagePath
        self.setText(GetImageFileNameFromFilePath(imagePath))


@as_dependency(Project, Application)
class ProjectWidgetViewModel:
    def __init__(
        self,
        project: Project,
        application: Application,
    ) -> None:
        self.project = project
        self.application = application

    def LoadImage(self, imagePath: str) -> None:
        imageName = GetImageFileNameFromFilePath(imagePath)
        imageName = GetImageNameBasedOnExistedImageNames(
            imageName,
            self.project.images,
        )
        self.project.images.append(imageName)

        targetPath = GetImageFilePath(
            self.application.CurrentProjectDirectory,
            imageName,
        )

        imageMetaPath = GetImageMetadataFile(
            self.application.CurrentProjectDirectory,
            imageName,
        )

        logger.debug(f"imageMetaPath: {imageMetaPath}")
        with open(imageMetaPath, "w") as f:
            f.write(ImageMeta().ToJson())

        shutil.copyfile(imagePath, targetPath)

        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)

    @property
    def ImageItems(self) -> list[QStandardItem]:
        return [ImageItem(image) for image in self.project.images]

    def DeleteImage(self, index: int) -> None:
        self.project.images.pop(index)
        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)
