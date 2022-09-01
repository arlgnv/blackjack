from typing import TypedDict, Optional, Literal
from enum import Enum


class EventNames(Enum):
    GAME_STARTED = 'gameStarted'
    BET_MADE = 'betMade'
    CARD_ISSUED = 'cardIssued'
    GAME_FINISHED = 'gameFinished'
    GAME_RESTARTED = 'gameRestarted'


class GameStages(str, Enum):
    STARTING_IS_AWAITED = 'startingIsAwaited'
    BET_IS_AWAITED = 'betIsAwaited'
    CARD_TAKING_IS_AWAITED = 'cardTakingIsAwaited'
    FINISHED = 'finished'


class PlayerNames(str, Enum):
    COMPUTER = 'skynet'
    HUMAN = 'player'


class Player(TypedDict):
    money: int
    deck: list[int]
    score: int


class Game(TypedDict):
    stage: Literal[
        GameStages.STARTING_IS_AWAITED,
        GameStages.BET_IS_AWAITED,
        GameStages.CARD_TAKING_IS_AWAITED,
        GameStages.FINISHED
    ]
    deck: list[int]
    bank: int
    winner: Optional[PlayerNames]
    skynet: Player
    player: Player
