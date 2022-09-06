from typing import Callable

from layers.view import types as view_types
from layers.model import types as model_types


EventName = view_types.EventName | model_types.EventName
Observers = dict[EventName, list[Callable[..., None]]]
