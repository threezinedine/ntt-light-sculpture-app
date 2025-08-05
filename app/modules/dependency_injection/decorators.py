from typing import TypeVar
from modules.dependency_injection import DependencyContainer

T = TypeVar("T")


def as_singleton(cls: type[T]) -> type[T]:
    DependencyContainer.RegisterSingleton(cls.__name__, cls())
    return cls


def as_transition(cls: type[T]) -> type[T]:
    DependencyContainer.RegisterTransition(cls.__name__, lambda: cls())
    return cls
