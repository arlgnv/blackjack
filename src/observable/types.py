from enum import Enum
from typing import Literal, Callable


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    BET_MADE = 'betMade'
    CARD_TAKEN = 'cardTaken'
    CARD_REJECTED = 'cardRejected'


EventName = Literal[EventNames.GAME_STARTED, EventNames.BET_MADE,
                    EventNames.CARD_TAKEN, EventNames.CARD_REJECTED]
Observers = dict[EventName, list[Callable[..., None]]]
