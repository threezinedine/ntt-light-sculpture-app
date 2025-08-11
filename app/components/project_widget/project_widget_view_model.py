from PyQt6.QtGui import QStandardItem
from constants import MODIFY_IMAGES_LIST_EVENT_NAME
from structs.project import Project
from modules.dependency_injection.helper import as_dependency
from modules.event_system.event_system import EventSystem
from utils.application import GetImageFileNameFromFilePath


class ImageItem(QStandardItem):
    def __init__(
        self,
        imagePath: str,
    ) -> None:
        super().__init__()
        self.imagePath = imagePath
        self.setText(GetImageFileNameFromFilePath(imagePath))


@as_dependency(Project)
class ProjectWidgetViewModel:
    def __init__(
        self,
        project: Project,
    ) -> None:
        self.project = project

    def LoadImage(self, imagePath: str) -> None:
        self.project.imagePaths.append(imagePath)
        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)

    @property
    def ImageItems(self) -> list[QStandardItem]:
        return [ImageItem(imagePath) for imagePath in self.project.imagePaths]

    def DeleteImage(self, index: int) -> None:
        self.project.imagePaths.pop(index)
        EventSystem.TriggerEvent(MODIFY_IMAGES_LIST_EVENT_NAME)
