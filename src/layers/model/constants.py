from shared.constants import DECK

from layers.model.types import State

DEFAULT_STATE: State = {
    'is_finished': False,
    'winner': None,
    'deck': DECK.copy(),
    'bank': 0,
    'skynet': {
        'deck': [],
        'score': 0,
        'money': 0
    },
    'player': {
        'deck': [],
        'score': 0,
        'money': 10
    },
}
WIN_SCORE = 21
MAX_CARDS_NUMBER_ON_HAND = 5
COMPUTER_NAME = 'skynet'
