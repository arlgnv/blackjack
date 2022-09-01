from .types import Game, GameStages

DECK = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 6, 6, 6, 6, 7, 7,
        7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]
DEFAULT_STATE: Game = {
    'stage': GameStages.GAME_STARTING_IS_AWAITED,
    'deck': DECK.copy(),
    'bank': 0,
    'winner': None,
    'skynet': {
        'money': 0,
        'deck': [],
        'score': 0,
    },
    'player': {
        'money': 0,
        'deck': [],
        'score': 0,
    },
}
WIN_SCORE = 21
MAX_CARDS_NUMBER_ON_HAND = 5
