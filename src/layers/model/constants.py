from shared.constants import DECK

from layers.model.types import State

DEFAULT_STATE: State = {
    'deck': DECK.copy(),
    'bank': 0,
    'skynet': {
        'deck': [],
        'score': 0,
    },
    'player': {
        'deck': [],
        'score': 0,
        'money': 10
    },
}
MAX_CARDS_NUMBER_ON_HAND = 5
