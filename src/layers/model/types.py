from enum import Enum
from typing import TypedDict, Optional, Literal

PlayerName = Literal['skynet', 'player']


class GameStages(Enum):
    GAME_STARTING_IS_AWAITED = 'gameStartingIsAwaited'
    BET_IS_AWAITED = 'betIsAwaited'
    CARD_TAKING_IS_AWAITED = 'cardTakingIsAwaited'
    FINISHED = 'finished'


class PlayerNames(Enum):
    SKYNET = 'skynet'
    PLAYER = 'player'


class Player(TypedDict):
    money: int
    deck: list[int]
    score: int


class Game(TypedDict):
    stage: Literal['gameStartingIsAwaited',
                   'betIsAwaited', 'cardTakingIsAwaited', 'finished']
    deck: list[int]
    bank: int
    winner: Optional[PlayerName]
    skynet: Player
    player: Player
