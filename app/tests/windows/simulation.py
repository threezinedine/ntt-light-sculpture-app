from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPointF, QEvent, Qt
from PyQt6.QtGui import QMouseEvent
from pytestqt.qtbot import QtBot


def simulateMouseDrag(
    qtBot: QtBot,
    widget: QWidget,
    startPosition: tuple[int, int],
    endPosition: tuple[int, int],
    numberOfSteps: int = 10,
    delay: float = 0.1,
) -> None:
    """
    This is the blocking simulation
    """
    startPos = QPointF(*startPosition)
    endPos = QPointF(*endPosition)

    dx = (endPos.x() - startPos.x()) / numberOfSteps
    dy = (endPos.y() - startPos.y()) / numberOfSteps

    pressEvent = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        startPos,
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mousePressEvent(pressEvent)

    stepCount = 0
    while True:
        stepCount += 1
        currentPos = QPointF(
            startPos.x() + dx * stepCount,
            startPos.y() + dy * stepCount,
        )
        moveEvent = QMouseEvent(
            QEvent.Type.MouseMove,
            currentPos,
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        widget.mouseMoveEvent(moveEvent)

        qtBot.wait(int(delay * 1000))

        if stepCount >= numberOfSteps:
            break

    releaseEvent = QMouseEvent(
        QEvent.Type.MouseButtonRelease,
        endPos,
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    widget.mouseReleaseEvent(releaseEvent)
