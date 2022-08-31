from typing import Callable, Optional, Any

from .types import Observers, EventName


class Observable:
    def __init__(self) -> None:
        self._observers: Observers = {}

    def subscribe(self, event_name: EventName, callback: Callable[..., None]) -> None:
        if event_name in self._observers:
            self._observers[event_name].append(callback)
        else:
            self._observers[event_name] = [callback]

    def notify(self, event_name: EventName, args: Optional[Any] = None) -> None:
        for callback in self._observers[event_name]:
            if args == None:
                callback()
            else:
                callback(args)
