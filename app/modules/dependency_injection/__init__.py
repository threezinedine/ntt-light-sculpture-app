from typing import Any, Callable
from utils.logger import logger


class DependencyContainer:
    """
    The module stores and manages the passed instances through the whole application.
    There are two types of instances:
    1. Singleton: The instance is created once and is used throughout the application.
    2. Transient: The instance is created every time it is requested.
    """

    _singletons: dict[str, Any] = {}
    _transitions: dict[str, Callable[..., Any]] = {}

    @staticmethod
    def Clear() -> None:
        """
        Clear the container.
        """
        DependencyContainer._singletons.clear()
        DependencyContainer._transitions.clear()

    @staticmethod
    def RegisterSingleton(name: str, instance: Any) -> None:
        """
        Add the singleton instance to the container.
        If the instance is already in the container, it will be replaced.

        Args:
            name: The name of the instance. This name is unique in the container. If the
                name is already in the container, a warning will be logged.
            instance: The instance to be added to the container.
        """
        if name in DependencyContainer._transitions:
            content = f"Transition with name {name} already exists. The singleton will not be registered."
            logger.fatal(content)
            raise ValueError(content)
        if name in DependencyContainer._singletons:
            content = f"Singleton with name {name} already exists. The instance will be replaced."
            logger.warning(content)
        DependencyContainer._singletons[name] = instance

    @staticmethod
    def RegisterTransition(name: str, factory: Callable[..., Any]) -> None:
        """
        Add the transition instance to the container.
        The transition instance is created every time it is requested.

        Args:
            name: The name of the instance. This name is unique in the container. If the
                name is already in the container, a warning will be logged.
            factory: The factory function to create the instance. The factory function
                can accept any number of arguments. The arguments will be passed to the
                factory function when the instance is created.
        """
        if name in DependencyContainer._singletons:
            content = f"Singleton with name {name} already exists. The transition will not be registered."
            logger.fatal(content)
            raise ValueError(content)
        if name in DependencyContainer._transitions:
            content = f"Transition with name {name} already exists. The instance will be replaced."
            logger.warning(content)
        DependencyContainer._transitions[name] = factory

    @staticmethod
    def GetInstance(name: str) -> Any:
        """
        Get the instance from the container. Even if the is singleton or transition,
        the instance will be returned.

        Args:
            name: The name of the instance.
        """
        if name in DependencyContainer._singletons:
            return DependencyContainer._singletons[name]
        elif name in DependencyContainer._transitions:
            return DependencyContainer._transitions[name]()
        else:
            content = f"Instance with name {name} not found"
            logger.fatal(content)
            raise ValueError(content)
