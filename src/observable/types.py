from typing import Literal, Callable


EventName = Literal["betMade"] | Literal["cardTaken"]
Observers = dict[EventName, list[Callable[..., None]]]
