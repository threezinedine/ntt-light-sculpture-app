from modules.dependency_injection.helper import as_dependency
from structs.project import Project


@as_dependency(Project)
class ImagePreviewViewModel:
    def __init__(self, project: Project):
        self._index = 0
        self._project = project

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
