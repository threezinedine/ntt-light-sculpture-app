from modules.dependency_injection.helper import as_dependency
from modules.history_manager import HistoryManager
from structs.project import Project
from .commands import ChangeDrawEdgesCommand, ChangeDrawFacesCommand
from Engine import Position, Renderer, Camera


@as_dependency(Project)
class OpenGLSettingViewModel:
    def __init__(self, project: Project) -> None:
        self.project = project
        self.openglSetting = project.openglSetting

    def Config(self) -> None:
        Renderer.SetShouldDrawEdges(self.openglSetting.drawEdges)
        Renderer.SetShouldDrawFaces(self.openglSetting.drawFaces)
        origin = self.openglSetting.origin
        Camera.SetOrigin(Position(origin[0], origin[1], origin[2]))

    @property
    def DrawEdges(self) -> bool:
        return self.openglSetting.drawEdges

    def SetDrawEdges(self, value: bool, propagate: bool = True) -> None:
        if propagate:
            HistoryManager.Execute(ChangeDrawEdgesCommand(self.project, value))
        else:
            self.openglSetting.drawEdges = value

        Renderer.SetShouldDrawEdges(value)

    @property
    def DrawFaces(self) -> bool:
        return self.openglSetting.drawFaces

    def SetDrawFaces(self, value: bool, propagate: bool = True) -> None:
        if propagate:
            HistoryManager.Execute(ChangeDrawFacesCommand(self.project, value))
        else:
            self.openglSetting.drawFaces = value

        Renderer.SetShouldDrawFaces(value)
