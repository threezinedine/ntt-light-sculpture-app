from typing import Any, Callable, List, TypeVar, Type
from modules.dependency_injection import DependencyContainer
from utils.logger import logger

T = TypeVar("T")


def as_singleton(cls: type[T]) -> type[T]:
    logger.debug(f'Registering singleton: "{cls.__name__}"')

    arguments: List[Any] = []

    if cls.__name__ in DependencyContainer._dependencies:  # type: ignore
        dependencies = DependencyContainer._dependencies[cls.__name__]  # type: ignore

        for dependency in dependencies:
            if dependency in DependencyContainer._transitions:  # type: ignore
                logger.warning(
                    f'Transition "{dependency}" is registered as a dependency of "{cls.__name__}" which is a singleton'
                )

            arguments.append(DependencyContainer.GetInstance(dependency))

    DependencyContainer.RegisterSingleton(cls.__name__, cls(*arguments))
    return cls


def as_transition(cls: type[T]) -> type[T]:

    def transition_factory(cls: type[T]) -> T:
        arguments: List[Any] = []
        if cls.__name__ in DependencyContainer._dependencies:  # type: ignore
            dependencies = DependencyContainer._dependencies[cls.__name__]  # type: ignore

            for dependency in dependencies:
                arguments.append(DependencyContainer.GetInstance(dependency))

        return cls(*arguments)

    DependencyContainer.RegisterTransition(
        cls.__name__, lambda: transition_factory(cls)
    )
    return cls


def as_dependency(*classes: ...) -> Callable[[Type[T]], Type[T]]:
    def dependency_decorator(cls: Type[T]) -> Type[T]:
        if cls.__name__ not in DependencyContainer._dependencies:  # type: ignore
            DependencyContainer._dependencies[cls.__name__] = []  # type: ignore

        for class_ in classes:
            DependencyContainer._dependencies[cls.__name__].append(class_.__name__)  # type: ignore

        return cls

    return dependency_decorator
