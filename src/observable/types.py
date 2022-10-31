from typing import Callable

from layers.view.types import EventName as ViewEventName
from layers.model.types import EventName as ModelEventName


EventName = ViewEventName | ModelEventName
Observers = dict[EventName, list[Callable[..., None]]]
