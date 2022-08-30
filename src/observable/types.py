from typing import Literal, Callable


EventName = Literal['betMade', 'cardTaken', 'gameFinished']
Observers = dict[EventName, list[Callable[..., None]]]
