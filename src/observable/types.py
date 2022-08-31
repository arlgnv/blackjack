from enum import Enum
from typing import Literal, Callable


EventName = Literal['gameStarted', 'betMade', 'cardTaken', 'gameFinished']
Observers = dict[EventName, list[Callable[..., None]]]


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    BET_MADE = 'betMade'
    CARD_TAKEN = 'cardTaken'
    GAME_FINISHED = 'gameFinished'
