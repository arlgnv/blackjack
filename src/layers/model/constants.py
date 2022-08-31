from shared.constants import DECK

from .types import Game, GameStages

DEFAULT_STATE: Game = {
    'stage': GameStages.GAME_STARTING_IS_AWAITED.value,
    'deck': DECK.copy(),
    'bank': 0,
    'winner': None,
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
