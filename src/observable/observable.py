from typing import Callable, Optional, Any

from .types import Observers, EventName


class Observable:
    _observers: Observers

    def __init__(self) -> None:
        self._observers = {}

    def on(self, event_name: EventName, callback: Callable[..., None]) -> None:
        if event_name in self._observers:
            self._observers[event_name].append(callback)
        else:
            self._observers[event_name] = [callback]

    def _emit(self, event_name: EventName, args: Optional[Any] = None) -> None:
        if event_name in self._observers:
            for callback in self._observers[event_name]:
                if args is None:
                    callback()
                else:
                    callback(args)
