from enum import Enum


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    MONEY_DEPOSITED = 'moneyDeposited'
    BET_MADE = 'betMade'
    CARD_TAKEN = 'cardTaken'
    CARD_REJECTED = 'cardRejected'
    GAME_RESTARTED = 'gameRestarted'
