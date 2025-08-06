from typing import Any, Callable, List, TypeVar, Type
from modules.dependency_injection import DependencyContainer
from utils.logger import logger

T = TypeVar("T")


def as_singleton(cls: type[T]) -> type[T]:
    """
    Used for annotating a class be used as a singleton inside the current project.

    Example:
    ```python
    @as_singleton
    class SingletonClass:
        def __init__(self) -> None:
            self.value: int = 0
    ```

    For now other class which is used `@as_transition` or `@as_singleton` can retrieve the
        global instance of the `SingletonClass` via the constructor
    """
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
    """
    Used for annotating a class be used as a transition inside the current project.
    The dependencies are listed before other arguments.

    Example:
    ```python
    @as_transition
    class TransitionClass:
        def __init__(self) -> None:
            self.value: int = 0
    ```

    For now other class which is used `@as_transition` or `@as_singleton` can retrieve the
        new instance of the `TransitionClass` via the constructor
    """

    def transition_factory(cls: type[T], *args: Any, **kwargs: Any) -> T:
        arguments: List[Any] = []
        if cls.__name__ in DependencyContainer._dependencies:  # type: ignore
            dependencies = DependencyContainer._dependencies[cls.__name__]  # type: ignore

            for dependency in dependencies:
                arguments.append(DependencyContainer.GetInstance(dependency))

        return cls(*arguments, *args, **kwargs)

    DependencyContainer.RegisterTransition(
        cls.__name__, lambda *args, **kwargs: transition_factory(cls, *args, **kwargs)
    )
    return cls


def as_dependency(*classes: ...) -> Callable[[Type[T]], Type[T]]:
    """
    Be used for annotating a class be used as a dependency of another class.
    This decorator can be used with `@as_transition` or `@as_singleton` decorators but
        no effect is active, must be used with `@as_transition` or `@as_singleton` decorators
        for the dependency to be used.

    Example:
    ```python
    @as_transition
    @as_dependency(TransitionClass) # the as_dependency must be behind the as_transition decorator
    class DependencyClass:
        def __init__(self, transition: TransitionClass) -> None:
            self.transition = transition
    ```
    """

    def dependency_decorator(cls: Type[T]) -> Type[T]:
        if cls.__name__ not in DependencyContainer._dependencies:  # type: ignore
            DependencyContainer._dependencies[cls.__name__] = []  # type: ignore

        for class_ in classes:
            DependencyContainer._dependencies[cls.__name__].append(class_.__name__)  # type: ignore

        return cls

    return dependency_decorator
