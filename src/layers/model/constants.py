from shared.constants import DECK


DEFAULT_STATE = {
    'deck': DECK.copy(),
    'bank': 0,
    'computer': {
        'deck': [],
        'score': 0,
    },
    'player': {
        'deck': [],
        'score': 0,
        'money': 10
    },
}
