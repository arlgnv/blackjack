from .types import State, GameStages

DECK = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7,
        7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]
INITIAL_STATE: State = {
    'game': {
        'stage': GameStages.FIRST_STARTING_IS_AWAITED.value,
        'deck': DECK.copy(),
        'bank': 0,
        'winner': None,
        'computer': {
            'deck': [],
            'score': 0,
        },
        'player': {
            'deck': [],
            'score': 0,
        },
    },
    'statistics': {
        'computer': {
            'wins': 0,
        },
        'player': {
            'money': 50,
            'wins': 0,
        },
    }
}
WIN_SCORE = 21
MAX_CARDS_NUMBER_ON_HAND = 5
MIN_BET = 0
SCORE_WORTH_RISK = 17
SCORE_NOT_WORTH_RISK = 19
