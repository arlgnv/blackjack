from typing import Literal, Callable


EventName = Literal['gameStarted', 'betMade', 'cardTaken', 'gameFinished']
Observers = dict[EventName, list[Callable[..., None]]]
