from typing import Literal, TypedDict, Optional
from enum import Enum


class GameStages(Enum):
    FIRST_STARTING_IS_AWAITED = 'firstStartingIsAwaited'
    STARTING_IS_AWAITED = 'startingIsAwaited'
    DEPOSIT_IS_AWAITED = 'depositIsAwaited'
    BET_IS_AWAITED = 'betIsAwaited'
    CARD_TAKING_IS_AWAITED = 'cardTakingIsAwaited'
    FINISHED = 'finished'


GameStage = Literal['firstStartingIsAwaited', 'startingIsAwaited',
                    'depositIsAwaited', 'betIsAwaited',
                    'cardTakingIsAwaited', 'finished']


class PlayerNames(Enum):
    COMPUTER = 'computer'
    PLAYER = 'player'


PlayerName = Literal['computer', 'player']


class ComputerStatistics(TypedDict):
    wins: int


class PlayerStatistics(TypedDict):
    money: int
    wins: int


class Statistics(TypedDict):
    computer: ComputerStatistics
    player: PlayerStatistics


class Computer(TypedDict):
    deck: list[int]
    score: int


class Player(TypedDict):
    deck: list[int]
    score: int


class Game(TypedDict):
    stage: GameStage
    deck: list[int]
    bank: int
    winner: Optional[PlayerName]
    computer: Computer
    player: Player


class State(TypedDict):
    game: Game
    statistics: Statistics


class EventNames(Enum):
    STATE_UPDATED = 'stateUpdated'
