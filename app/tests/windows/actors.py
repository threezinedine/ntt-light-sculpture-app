from typing import Generator, Self
from PyQt6.QtCore import QAbstractItemModel, Qt
from PyQt6.QtWidgets import QMenu, QTabWidget
from pyfakefs.fake_filesystem import FakeFilesystem
import pytest
from pytestqt.qtbot import QtBot

from components.customs.tree_view.tree_view import CustomTreeView
from components.image_preview_widget.image_preview_widget import ImagePreviewWidget
from constants import IMAGE_CONTEXT_DELETE_OPTION, IMAGE_CONTEXT_OPEN_OPTION
from utils.logger import logger  # type: ignore
from windows.main_window import MainWindow


class MainWindowActor:
    def __init__(self, qtbot: QtBot) -> None:
        self.qtbot = qtbot
        self._mainWindow: MainWindow | None = None

    def SetMainWindow(self, mainWindow: MainWindow) -> Self:
        self._mainWindow = mainWindow
        return self

    def SaveWindow(self) -> Self:
        assert (
            self._mainWindow is not None
        ), "The main window must be set before using SaveWindow"

        self._mainWindow.ui.saveProjectAction.trigger()
        return self


@pytest.fixture()
def mainWindowActor(qtbot: QtBot) -> Generator[MainWindowActor, None, None]:
    yield MainWindowActor(qtbot)


class ProjectTreeActor:
    def __init__(
        self,
        qtbot: QtBot,
    ) -> None:
        self.qtbot = qtbot
        self.projectTreeView: CustomTreeView | None = None

        self._model: QAbstractItemModel | None = None
        self._contextMenu: QMenu | None = None

    def SetProjectTreeView(self, projectTreeView: CustomTreeView) -> Self:
        self.projectTreeView = projectTreeView
        self._model = self.projectTreeView.model()
        return self

    @property
    def NumberOfRows(self) -> int:
        assert self.projectTreeView is not None
        assert self._model is not None
        self._model = self.projectTreeView.model()
        return self._model.rowCount()

    def GetItemNameAt(self, index: int) -> str:
        assert self.projectTreeView is not None
        assert self._model is not None
        return self._model.index(index, 0).data(Qt.ItemDataRole.DisplayRole)

    def OpenContextMenuAt(self, index: int) -> Self:
        assert self.projectTreeView is not None
        assert self._model is not None

        item = self._model.index(index, 0)
        itemRect = self.projectTreeView.visualRect(item)
        self.qtbot.mouseClick(  # type: ignore
            self.projectTreeView.viewport(),
            Qt.MouseButton.RightButton,
            pos=itemRect.center(),
        )

        self.qtbot.wait(100)

        self._contextMenu = self.projectTreeView.findChild(QMenu)  # type: ignore
        assert self._contextMenu is not None

        return self

    def _ChooseContextMenuAction(self, actionName: str) -> None:
        assert self.projectTreeView is not None
        assert self._contextMenu is not None, "Context menu is not open"
        actions = self._contextMenu.actions()
        action = next((a for a in actions if a.text() == actionName), None)
        assert action is not None
        action.trigger()

    def ChooseDeleteAction(self) -> Self:
        self._ChooseContextMenuAction(IMAGE_CONTEXT_DELETE_OPTION)
        return self

    def ChooseOpenImageTabAction(self) -> Self:
        self._ChooseContextMenuAction(IMAGE_CONTEXT_OPEN_OPTION)
        return self


@pytest.fixture()
def projectTreeActor(
    qtbot: QtBot,
) -> Generator[ProjectTreeActor, None, None]:
    yield ProjectTreeActor(qtbot)


class TabWidgetActor:
    def __init__(self, qtbot: QtBot, fs: FakeFilesystem | None = None) -> None:
        self.qtbot = qtbot
        self.fs = fs

        self._tabWidget: QTabWidget | None = None

    def SetTabWidget(self, tabWidget: QTabWidget) -> Self:
        self._tabWidget = tabWidget
        return self

    def CloseTabWithName(self, name: str) -> Self:
        assert self._tabWidget is not None
        for i in range(self._tabWidget.count()):
            if self._tabWidget.tabText(i) == name:
                self._tabWidget.tabCloseRequested.emit(i)
                break

        return self


@pytest.fixture()
def tabWidgetActor(
    qtbot: QtBot,
) -> Generator[TabWidgetActor, None, None]:
    yield TabWidgetActor(qtbot)


class ImagePreviewWidgetActor:
    def __init__(self, qtbot: QtBot) -> None:
        self.qtbot = qtbot
        self._imagePreviewWidget: ImagePreviewWidget | None = None

    def SetImagePreviewWidget(self, imagePreviewWidget: ImagePreviewWidget) -> Self:
        self._imagePreviewWidget = imagePreviewWidget
        return self

    def AssertThresholdSliderValue(self, value: int) -> Self:
        assert self._imagePreviewWidget is not None
        thresholdSliderValue = self._imagePreviewWidget.ui.thresholdSlider.value()
        assert (
            thresholdSliderValue == value
        ), f"Threshold value is {thresholdSliderValue}, expected {value} but got {thresholdSliderValue}"
        return self

    def DragThresholdSlider(self, value: int) -> Self:
        assert self._imagePreviewWidget is not None
        self._imagePreviewWidget.ui.thresholdSlider.setValue(value)
        self.qtbot.wait(100)
        self._imagePreviewWidget.ui.thresholdSlider.sliderReleased.emit()
        return self


@pytest.fixture()
def imagePreviewWidgetActor(
    qtbot: QtBot,
) -> Generator[ImagePreviewWidgetActor, None, None]:
    yield ImagePreviewWidgetActor(qtbot)
