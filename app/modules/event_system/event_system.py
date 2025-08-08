from typing import Any, Callable, TypeAlias
from utils.logger import logger

EventCallback: TypeAlias = Callable[..., None]


class EventSystem:
    """
    Event system is the center hub which store and notify all the event inside the project, this module
        also support the attaching the event to another one, whereas when the first event is triggered,
        it also trigger the second event, vice versa, each event will be triggered only once even if it has
        the circular dependency (but the warning will be logged).

        The event can be registered by the event name and all callbacks which attached to the event will be
        triggered when the event is triggered.

    Examples:
    ```python
        EventSystem.TriggerEvent("event_name", *args, **kwargs) # now no callback is attached to the event and nothing will happen

        EventSystem.RegisterEvent("event_name", callback) # now the callback will be triggered when the event is triggered

        EventSystem.RegisterEvent("event_name", callback) # now the callback will be triggered when the event is triggered
    ```
    """

    _callbackMap: dict[str, list[EventCallback]] = {}
    _eventDependencyMap: dict[str, set[str]] = {}

    _triggeredEventStack: list[str] = (
        []
    )  # the stack which is used for checking and avoid the circular dependency trigger, must be empty when the event is triggered, and be cleared after the event is triggered

    @staticmethod
    def RegisterEvent(eventName: str, callback: EventCallback):
        """
        Attach the callback to the current system, whereas if the `eventName` is triggered, the callback will be triggered.

        Args:
            eventName (str): The name of the event to register. No need to be existed inside the system,
                but the callback will be triggered when the event is triggered.
            callback (EventCallback): The callback to be triggered when the event is triggered. This method will
                received anything.
        """
        if eventName not in EventSystem._callbackMap:
            EventSystem._callbackMap[eventName] = []

        EventSystem._callbackMap[eventName].append(callback)

    @staticmethod
    def TriggerEvent(eventName: str, *args: Any, **kwargs: Any):
        """
        Trigger the event by the event name, whereas all callbacks which attached to the event will be triggered.

        Args:
            eventName (str): The name of the event to trigger. If the event is not registered, nothing will happen.
                The warning will be logged.
        """
        EventSystem._triggeredEventStack.clear()

        EventSystem._TriggerEventInternal(eventName, *args, **kwargs)

        EventSystem._triggeredEventStack.clear()

    @staticmethod
    def _TriggerEventInternal(eventName: str, *args: Any, **kwargs: Any):
        """
        The internal method which is used for triggering the event, and the circular dependency will be checked.
        """
        if eventName in EventSystem._triggeredEventStack:
            return

        EventSystem._triggeredEventStack.append(eventName)

        if eventName not in EventSystem._callbackMap:
            logger.warning(
                f'Event "{eventName}" is not registered, nothing will happen.'
            )
        else:
            for callback in EventSystem._callbackMap[eventName]:
                callback(*args, **kwargs)

        if eventName not in EventSystem._eventDependencyMap:
            return

        for dependencyEventName in EventSystem._eventDependencyMap[eventName]:
            EventSystem._TriggerEventInternal(dependencyEventName, *args, **kwargs)

    @staticmethod
    def AttachEvent(eventName: str, *dependencyEventNames: str):
        """
        Attach an event to another one, whereas when the first event is triggered, it also trigger the second event.
            vice versa, each event will be triggered only once even if it has the circular dependency (but the warning will be logged).

        Args:
            eventName (str): The name of the event to attach. No need to be existed inside the system.
            *dependencyEventNames (str): The listing of all event which will be attached to the `eventName`.
        """
        if eventName not in EventSystem._eventDependencyMap:
            EventSystem._eventDependencyMap[eventName] = set()

        EventSystem._eventDependencyMap[eventName].update(dependencyEventNames)

        for dependencyEventName in dependencyEventNames:
            if dependencyEventName not in EventSystem._eventDependencyMap:
                EventSystem._eventDependencyMap[dependencyEventName] = set()

            EventSystem._eventDependencyMap[dependencyEventName].add(eventName)

    @staticmethod
    def Clear() -> None:
        EventSystem._callbackMap.clear()
        EventSystem._eventDependencyMap.clear()
        EventSystem._triggeredEventStack.clear()
