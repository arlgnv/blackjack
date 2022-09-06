from typing import Callable, Optional, Any

from . import types


class Observable:
    _observers: types.Observers

    def __init__(self) -> None:
        self._observers: types.Observers = {}

    def on(self, event_name: types.EventName, callback: Callable[..., None]) -> None:
        if event_name in self._observers:
            self._observers[event_name].append(callback)
        else:
            self._observers[event_name] = [callback]

    def _emit(self, event_name: types.EventName, args: Optional[Any] = None) -> None:
        if event_name in self._observers:
            for callback in self._observers[event_name]:
                if args is None:
                    callback()
                else:
                    callback(args)
