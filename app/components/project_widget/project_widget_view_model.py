import shutil
from PyQt6.QtGui import QStandardItem
from constants import MODIFY_IMAGES_LIST_EVENT_NAME
from structs.application import Application
from structs.project import Project
from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from utils.application import GetImageFileNameFromFilePath, GetImageFilePath


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
        self.project.images.append(imageName)

        print(self.application.CurrentProjectDirectory)
        targetPath = GetImageFilePath(
            self.application.CurrentProjectDirectory,
            imageName,
        )

        shutil.copyfile(imagePath, targetPath)

        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)

    @property
    def ImageItems(self) -> list[QStandardItem]:
        return [ImageItem(image) for image in self.project.images]

    def DeleteImage(self, index: int) -> None:
        self.project.images.pop(index)
        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)
