from enum import Enum
from typing import Literal, Callable


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    BET_MADE = 'betMade'
    CARD_TAKEN = 'cardTaken'
    ENOUGH_SAID = 'enoughSaid'
    GAME_FINISHED = 'gameFinished'


EventName = Literal[EventNames.GAME_STARTED, EventNames.BET_MADE,
                    EventNames.CARD_TAKEN, EventNames.ENOUGH_SAID, EventNames.GAME_FINISHED]
Observers = dict[EventName, list[Callable[..., None]]]
