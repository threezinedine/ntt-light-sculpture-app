from typing import Generator
from abc import ABC, abstractmethod
import pytest
from modules.dependency_injection import DependencyContainer
from modules.dependency_injection.decorators import (
    as_singleton,
    as_transition,
    as_dependency,
)
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
        DependencyTestClass,
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
        DependencyTestClass,
    )

    with pytest.raises(ValueError):
        DependencyContainer.RegisterTransition(
            DependencyTestClass.__name__,
            lambda: DependencyTestClass(),
        )
    mockFatal.assert_called_once()


@patch("utils.logger.logger.fatal")
def test_register_transition_with_same_name_as_initialized_singleton_factory(
    mockFatal: MagicMock,
) -> None:
    DependencyContainer.RegisterSingleton(
        DependencyTestClass.__name__,
        DependencyTestClass,
    )

    with pytest.raises(ValueError):
        DependencyContainer.GetInstance(DependencyTestClass.__name__)

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
    @as_singleton()
    class SingletonClass:
        count: int = 0

        def __new__(cls) -> "SingletonClass":
            cls.count += 1
            return super().__new__(cls)

    DependencyContainer.GetInstance(SingletonClass.__name__)
    DependencyContainer.GetInstance(SingletonClass.__name__)

    assert SingletonClass.count == 1


def test_register_object_using_decorator_with_parameters() -> None:
    @as_transition()
    class TransitionClass:
        count: int = 0

        def __new__(cls) -> "TransitionClass":
            cls.count += 1
            return super().__new__(cls)

    DependencyContainer.GetInstance(TransitionClass.__name__)
    DependencyContainer.GetInstance(TransitionClass.__name__)

    assert TransitionClass.count == 2


def test_register_object_as_singleton_and_its_dependency() -> None:
    @as_singleton()
    class SingletonClass:
        count: int = 0

        def __new__(cls) -> "SingletonClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self) -> None:
            self.singletonValue = 0

    DependencyContainer.GetInstance(SingletonClass.__name__).singletonValue = 1994

    @as_singleton()
    @as_dependency(SingletonClass)
    class DependencyClass:
        count: int = 0

        def __new__(cls, singleton: "SingletonClass") -> "DependencyClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self, singleton: "SingletonClass") -> None:
            assert singleton.singletonValue == 1994
            self.value: int = 0

        def print(self) -> None:
            print(self.value)

    assert DependencyContainer.GetInstance(DependencyClass.__name__).count == 1
    assert DependencyContainer.GetInstance(SingletonClass.__name__).count == 1


@patch("utils.logger.logger.warning")
def test_register_transition_with_dependency(mockWarning: MagicMock) -> None:
    @as_transition()
    class TransitionClass:
        count: int = 0

        def __new__(cls) -> "TransitionClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self) -> None:
            self.value: int = 0

    DependencyContainer.GetInstance(TransitionClass.__name__).value = 1994

    @as_singleton()
    @as_dependency(TransitionClass)
    class SingletonClass:
        count: int = 0

        def __new__(cls, transition: "TransitionClass") -> "SingletonClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self, transition: "TransitionClass") -> None:
            assert transition.value == 0
            self.value: int = 0
            self.transition = transition
            transition.value = 1

    DependencyContainer.GetInstance(SingletonClass.__name__)

    assert TransitionClass.count == 2
    assert SingletonClass.count == 1
    assert DependencyContainer.GetInstance(TransitionClass.__name__).value == 0
    assert (
        DependencyContainer.GetInstance(SingletonClass.__name__).transition.value == 1
    )

    mockWarning.assert_called_once()  # warning while registering transition as singleton dependency


def test_register_transition_with_dependency_as_transition() -> None:
    @as_transition()
    class TransitionClass:
        count: int = 0

        def __new__(cls) -> "TransitionClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self) -> None:
            self.value: int = 0

    DependencyContainer.GetInstance(TransitionClass.__name__).value = 1994

    @as_transition()
    @as_dependency(TransitionClass)
    class TransitionClass2:
        count: int = 0

        def __new__(cls, transition: "TransitionClass") -> "TransitionClass2":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self, transition: "TransitionClass") -> None:
            assert transition.value == 0
            self.value: int = 0

    DependencyContainer.GetInstance(TransitionClass2.__name__)
    DependencyContainer.GetInstance(TransitionClass2.__name__)

    assert TransitionClass.count == 3
    assert TransitionClass2.count == 2


def test_get_transition_instance_with_arguments() -> None:
    @as_transition()
    class TransitionClass:
        count: int = 0

        def __new__(cls, value: int) -> "TransitionClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self, value: int) -> None:
            self.value = value

    assert DependencyContainer.GetInstance(TransitionClass.__name__, 3).value == 3


def test_get_singleton_instance_does_not_create_new_instance_until_it_is_requested() -> (
    None
):
    @as_singleton()
    class SingletonClass:
        count: int = 0

        def __new__(cls) -> "SingletonClass":
            cls.count += 1
            return super().__new__(cls)

    assert SingletonClass.count == 0

    DependencyContainer.GetInstance(SingletonClass.__name__)

    assert SingletonClass.count == 1


def test_register_singleton_with_different_name() -> None:
    class ISingleton(ABC):
        @property
        @abstractmethod
        def value(self) -> int:
            raise NotImplementedError

    @as_singleton(ISingleton)
    class SingletonClass(ISingleton):
        count: int = 0

        def __new__(cls) -> "SingletonClass":
            cls.count += 1
            return super().__new__(cls)

        def __init__(self) -> None:
            pass

        @property
        def value(self) -> int:
            return 1994

    instance: ISingleton = DependencyContainer.GetInstance(ISingleton.__name__)
    assert instance.value == 1994


def test_register_singleton_without_the_inheritance_of_the_interface() -> None:
    class ISingleton(ABC):
        @property
        @abstractmethod
        def value(self) -> int:
            raise NotImplementedError

    with pytest.raises(TypeError):

        @as_singleton(ISingleton)
        class SingletonClass:
            count: int = 0

            def __new__(cls) -> "SingletonClass":
                cls.count += 1
                return super().__new__(cls)


def test_register_transition_with_different_name() -> None:
    class ITransition(ABC):
        @property
        @abstractmethod
        def value(self) -> int:
            raise NotImplementedError

    @as_transition(ITransition)
    class TransitionClass(ITransition):
        def __new__(cls) -> "TransitionClass":
            return super().__new__(cls)

        @property
        def value(self) -> int:
            return 1994

    instance: ITransition = DependencyContainer.GetInstance(ITransition.__name__)
    assert instance.value == 1994


def test_register_transition_without_the_inheritance_of_the_interface() -> None:
    class ITransition(ABC):
        @property
        @abstractmethod
        def value(self) -> int:
            raise NotImplementedError

    with pytest.raises(TypeError):

        @as_transition(ITransition)
        class TransitionClass:
            def __new__(cls) -> "TransitionClass":
                return super().__new__(cls)

            @property
            def value(self) -> int:
                return 1994
