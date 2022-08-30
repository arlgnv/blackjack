from typing import TypedDict, Literal


class Player(TypedDict):
    money: int
    deck: list[int]
    score: int


class State(TypedDict):
    is_finished: bool
    deck: list[int]
    bank: int
    winner: Literal['player', 'skynet', None]
    skynet: Player
    player: Player


Subject = Literal['player', 'skynet']
