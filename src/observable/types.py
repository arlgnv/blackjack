from typing import Literal, Callable

from layers.view import EventNames as ViwEventNames
from layers.model import EventNames as ModelEventNames


EventName = Literal[ViwEventNames.GAME_STARTED, ViwEventNames.BET_MADE,
                    ViwEventNames.CARD_TAKEN, ViwEventNames.CARD_REJECTED, ViwEventNames.GAME_RESTARTED,
                    ModelEventNames.GAME_STARTED, ModelEventNames.BET_MADE,
                    ModelEventNames.CARD_ISSUED, ModelEventNames.GAME_FINISHED, ModelEventNames.GAME_RESTARTED,
                    ]
Observers = dict[EventName, list[Callable[..., None]]]
