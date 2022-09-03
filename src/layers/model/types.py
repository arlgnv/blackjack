from typing import TypedDict, Optional
from enum import Enum


class GameStages(str, Enum):
    FIRST_STARTING_IS_AWAITED = 'firstStartingIsAwaited'
    STARTING_IS_AWAITED = 'startingIsAwaited'
    DEPOSIT_IS_AWAITED = 'depositIsAwaited'
    BET_IS_AWAITED = 'betIsAwaited'
    CARD_TAKING_IS_AWAITED = 'cardTakingIsAwaited'
    FINISHED = 'finished'


class PlayerNames(str, Enum):
    COMPUTER = 'computer'
    PLAYER = 'player'


class Computer(TypedDict):
    deck: list[int]
    score: int
    wins: int


class Player(TypedDict):
    money: int
    deck: list[int]
    score: int
    wins: int


class Game(TypedDict):
    stage: GameStages
    deck: list[int]
    bank: int
    winner: Optional[PlayerNames]
    computer: Computer
    player: Player


class EventNames(Enum):
    GAME_STAGE_UPDATED = 'gameStageUpdated'
