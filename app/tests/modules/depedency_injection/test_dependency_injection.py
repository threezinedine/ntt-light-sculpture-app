from typing import Generator
import pytest
from modules.dependency_injection import DependencyContainer
from unittest.mock import MagicMock, patch


class DependencyTestClass:
    count: int = 0

    def __new__(cls) -> "DependencyTestClass":
        cls.count += 1
        return super().__new__(cls)

    def __init__(self) -> None:
        self.value: int = 0


@pytest.fixture(autouse=True)
def dj() -> Generator[None, None, None]:
    DependencyContainer.Clear()
    DependencyTestClass.count = 0
    yield
    DependencyContainer.Clear()


def test_register_singleton() -> None:
    DependencyContainer.RegisterSingleton(
        DependencyTestClass.__name__,
        DependencyTestClass(),
    )

    expectedValue = 23

    instance = DependencyContainer.GetInstance(DependencyTestClass.__name__)
    instance.value = expectedValue
    DependencyContainer.GetInstance(DependencyTestClass.__name__)

    assert DependencyTestClass.count == 1
    assert (
        DependencyContainer.GetInstance(DependencyTestClass.__name__).value
        == expectedValue
    )


def test_register_transition() -> None:
    DependencyContainer.RegisterTransition(
        DependencyTestClass.__name__, lambda: DependencyTestClass()
    )

    DependencyContainer.GetInstance(DependencyTestClass.__name__)
    DependencyContainer.GetInstance(DependencyTestClass.__name__).value = 23
    DependencyContainer.GetInstance(DependencyTestClass.__name__)

    assert DependencyTestClass.count == 3
    assert DependencyContainer.GetInstance(DependencyTestClass.__name__).value == 0


@patch("utils.logger.logger.warning")
def test_register_singleton_with_same_name(mockWarning: MagicMock) -> None:
    DependencyContainer.RegisterSingleton(
        DependencyTestClass.__name__,
        DependencyTestClass(),
    )
    DependencyContainer.RegisterSingleton(
        DependencyTestClass.__name__,
        DependencyTestClass(),
    )

    mockWarning.assert_called_once()


@patch("utils.logger.logger.warning")
def test_register_transition_with_same_name(mockWarning: MagicMock) -> None:
    DependencyContainer.RegisterTransition(
        DependencyTestClass.__name__,
        lambda: DependencyTestClass(),
    )
    DependencyContainer.RegisterTransition(
        DependencyTestClass.__name__,
        lambda: DependencyTestClass(),
    )
    mockWarning.assert_called_once()


@patch("utils.logger.logger.fatal")
def test_register_transition_with_same_name_as_singleton(mockFatal: MagicMock) -> None:
    DependencyContainer.RegisterSingleton(
        DependencyTestClass.__name__,
        DependencyTestClass(),
    )

    with pytest.raises(ValueError):
        DependencyContainer.RegisterTransition(
            DependencyTestClass.__name__,
            lambda: DependencyTestClass(),
        )
    mockFatal.assert_called_once()


@patch("utils.logger.logger.fatal")
def test_query_non_existent_instance(mockFatal: MagicMock) -> None:
    with pytest.raises(ValueError):
        DependencyContainer.GetInstance("NonExistentClass")

    mockFatal.assert_called_once()


def test_register_object_using_decorator() -> None:
    from .as_singleton import SingletonClass

    DependencyContainer.GetInstance(SingletonClass.__name__)
    DependencyContainer.GetInstance(SingletonClass.__name__)

    assert SingletonClass.count == 1


def test_register_object_using_decorator_with_parameters() -> None:
    from .as_transition import TransitionClass

    DependencyContainer.GetInstance(TransitionClass.__name__)
    DependencyContainer.GetInstance(TransitionClass.__name__)

    assert TransitionClass.count == 2
