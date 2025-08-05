from typing import Generator
import pytest
from modules.dependency_injection import DependencyContainer
from unittest.mock import MagicMock, patch


class DependencyTestClass:
    count: int = 0

    def __new__(cls) -> "DependencyTestClass":
        cls.count += 1
        return super().__new__(cls)


@pytest.fixture(autouse=True)
def dj() -> Generator[None, None, None]:
    DependencyContainer.Clear()
    DependencyTestClass.count = 0
    yield
    DependencyContainer.Clear()


def test_register_singleton() -> None:
    DependencyContainer.RegisterSingleton("DependencyTestClass", DependencyTestClass())

    DependencyContainer.GetInstance("DependencyTestClass")
    DependencyContainer.GetInstance("DependencyTestClass")
    DependencyContainer.GetInstance("DependencyTestClass")

    assert DependencyTestClass.count == 1


def test_register_transition() -> None:
    DependencyContainer.RegisterTransition(
        "DependencyTestClass", lambda: DependencyTestClass()
    )

    DependencyContainer.GetInstance("DependencyTestClass")
    DependencyContainer.GetInstance("DependencyTestClass")
    DependencyContainer.GetInstance("DependencyTestClass")

    assert DependencyTestClass.count == 3


@patch("utils.logger.logger.warning")
def test_register_singleton_with_same_name(mockWarning: MagicMock) -> None:
    DependencyContainer.RegisterSingleton("DependencyTestClass", DependencyTestClass())
    DependencyContainer.RegisterSingleton("DependencyTestClass", DependencyTestClass())

    mockWarning.assert_called_once()


@patch("utils.logger.logger.warning")
def test_register_transition_with_same_name(mockWarning: MagicMock) -> None:
    DependencyContainer.RegisterTransition(
        "DependencyTestClass", lambda: DependencyTestClass()
    )
    DependencyContainer.RegisterTransition(
        "DependencyTestClass", lambda: DependencyTestClass()
    )
    mockWarning.assert_called_once()


@patch("utils.logger.logger.fatal")
def test_register_transition_with_same_name_as_singleton(mockFatal: MagicMock) -> None:
    DependencyContainer.RegisterSingleton("DependencyTestClass", DependencyTestClass())

    with pytest.raises(ValueError):
        DependencyContainer.RegisterTransition(
            "DependencyTestClass", lambda: DependencyTestClass()
        )
    mockFatal.assert_called_once()
