from shared.constants import DECK

from .types import Game, GameStages

DEFAULT_STATE: Game = {
    'stage': GameStages.GAME_STARTING_IS_AWAITED,
    'deck': DECK.copy(),
    'bank': 0,
    'winner': None,
    'skynet': {
        'money': 0,
        'deck': [],
        'is_full': False,
        'score': 0,
    },
    'player': {
        'money': 10,
        'deck': [],
        'is_full': False,
        'score': 0,
    },
}
WIN_SCORE = 21
MAX_CARDS_NUMBER_ON_HAND = 5
