from enum import Enum


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    BET_MADE = 'betMade'
    CARD_TAKEN = 'cardTaken'
    CARD_REJECTED = 'cardRejected'
    GAME_RESTARTED = 'gameRestarted'
