from typing import Callable

from layers.view import EventNames as ViewEventNames
from layers.model import EventNames as ModelEventNames


EventName = ViewEventNames | ModelEventNames
Observers = dict[EventName, list[Callable[..., None]]]
