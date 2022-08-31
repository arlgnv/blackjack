from enum import Enum
from typing import TypedDict, Optional, Literal


class GameStages(Enum):
    GAME_STARTING_IS_AWAITED = 'gameStartingIsAwaited'
    BET_IS_AWAITED = 'betIsAwaited'
    CARD_TAKING_IS_AWAITED = 'cardTakingIsAwaited'
    FINISHED = 'finished'


class PlayerNames(Enum):
    SKYNET = 'skynet'
    PLAYER = 'player'


PlayerName = Literal[PlayerNames.SKYNET, PlayerNames.PLAYER]


class Player(TypedDict):
    money: int
    deck: list[int]
    score: int


class Game(TypedDict):
    stage: Literal[GameStages.GAME_STARTING_IS_AWAITED,
                   GameStages.BET_IS_AWAITED, GameStages.CARD_TAKING_IS_AWAITED, GameStages.FINISHED]
    deck: list[int]
    bank: int
    winner: Optional[PlayerName]
    winnings: Optional[int]
    skynet: Player
    player: Player
