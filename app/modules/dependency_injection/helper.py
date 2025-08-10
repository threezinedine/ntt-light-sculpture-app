from typing import Any, Callable, List, TypeVar, Type
from modules.dependency_injection import DependencyContainer
from utils.logger import logger

T = TypeVar("T")
V = TypeVar("V")


def as_singleton(cls: type[T], annotation: type[V] | None = None) -> None:
    """
    Used for annotating a class be used as a singleton inside the current project.

    Example:
    ```python
    class SingletonClass:
        def __init__(self) -> None:
            self.value: int = 0

    as_singleton(SingletonClass)
    ```

    For now other class which is used `as_transition` or `as_singleton` can retrieve the
        global instance of the `SingletonClass` via the constructor
    """
    logger.debug(f"Registering singleton: {cls.__name__}")

    def create_singleton(cls: type[T]) -> None:
        name = cls.__name__

        if annotation is not None:
            if not issubclass(cls, annotation):
                raise TypeError(
                    f'Class "{cls.__name__}" does not inherit from "{annotation.__name__}"'
                )
            name = annotation.__name__

        def singleton_factory(*args: Any, **kwargs: Any) -> Any:
            arguments: List[Any] = []

            if name in DependencyContainer._dependencies:  # type: ignore
                dependencies = DependencyContainer._dependencies[name]  # type: ignore

                for dependency in dependencies:
                    if dependency in DependencyContainer._transitions:  # type: ignore
                        logger.warning(
                            f'Transition "{dependency}" is registered as a dependency of "{name}" which is a singleton'
                        )

                    arguments.append(DependencyContainer.GetInstance(dependency))

            return cls(*arguments, *args, **kwargs)

        DependencyContainer.RegisterSingleton(name, singleton_factory)

    create_singleton(cls)


def as_transition(cls: type[T], annotation: type[V] | None = None) -> None:
    """
    Used for annotating a class be used as a transition inside the current project.
    The dependencies are listed before other arguments.

    Example:
    ```python
    class TransitionClass:
        def __init__(self) -> None:
            self.value: int = 0

    as_transition(TransitionClass)
    ```

    For now other class which is used `as_transition` or `as_singleton` can retrieve the
        new instance of the `TransitionClass` via the constructor
    """
    logger.debug(f"Registering transition: {cls.__name__}")

    def create_transition(cls: type[T]) -> None:
        name = cls.__name__

        if annotation is not None:
            if not issubclass(cls, annotation):
                raise TypeError(
                    f'Class "{cls.__name__}" does not inherit from "{annotation.__name__}"'
                )
            name = annotation.__name__

        def transition_factory(cls: type[T], *args: Any, **kwargs: Any) -> T:
            arguments: List[Any] = []
            if name in DependencyContainer._dependencies:  # type: ignore
                dependencies = DependencyContainer._dependencies[name]  # type: ignore

                for dependency in dependencies:
                    arguments.append(DependencyContainer.GetInstance(dependency))

            return cls(*arguments, *args, **kwargs)

        DependencyContainer.RegisterTransition(
            name,
            lambda *args, **kwargs: transition_factory(cls, *args, **kwargs),  # type: ignore
        )

    create_transition(cls)


def as_dependency(*classes: ...) -> Callable[[Type[T]], Type[T]]:
    """
    Be used for annotating a class be used as a dependency of another class.
    This decorator can be used with `as_transition` or `as_singleton` decorators but
        no effect is active, must be used with `as_transition` or `as_singleton` decorators
        for the dependency to be used.

    Example:
    ```python
    @as_dependency(TransitionClass) # the as_dependency must be behind the as_transition decorator
    class DependencyClass:
        def __init__(self, transition: TransitionClass) -> None:
            self.transition = transition

    as_transition(TransitionClass)
    ```
    """
    logger.debug(f"Registering dependency: {classes}")

    def dependency_decorator(cls: Type[T]) -> Type[T]:
        logger.debug(f"Registering dependency: {classes} for {cls.__name__}")
        if cls.__name__ not in DependencyContainer._dependencies:  # type: ignore
            DependencyContainer._dependencies[cls.__name__] = []  # type: ignore

        for class_ in classes:
            DependencyContainer._dependencies[cls.__name__].append(class_.__name__)  # type: ignore

        return cls

    return dependency_decorator
