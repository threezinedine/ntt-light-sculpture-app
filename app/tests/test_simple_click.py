from pytestqt.qtbot import QtBot
from PyQt6.QtCore import Qt
from views.widget_view import WidgetView


def test_simple_click(qtbot: QtBot):
    widget = WidgetView()
    qtbot.addWidget(widget)
    qtbot.mouseClick(widget.ui.testButton, Qt.MouseButton.LeftButton)  # type: ignore
