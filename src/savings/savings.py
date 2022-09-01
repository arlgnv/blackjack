from typing import Literal
from pathlib import Path
from os import path
from json import load, dump

from layers.model import Game, PlayerNames, EventNames as ModelEventNames
from layers.model.model import Model


class Savings:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._file_path = f'{Path(__file__).parent}/savings.json'

    def load_last_saved_game(self) -> Game | None:
        if self._check_if_file_exists():
            with open(self._file_path, 'r', encoding='utf-8') as savings_file:
                saved_game = load(savings_file)[0]
                winner: Literal['skynet',
                                'player'] | None = saved_game['winner']

                if winner:
                    saved_game['winner'] = PlayerNames(winner)

                return saved_game

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.GAME_STARTED,
                       self._handle_model_game_start)
        self._model.on(ModelEventNames.BET_MADE, self._handle_model_bet_make)
        self._model.on(ModelEventNames.CARD_ISSUED, self._handle_card_issue)
        self._model.on(ModelEventNames.GAME_FINISHED, self._handle_game_finish)

    def _save_game(self, game: Game) -> None:
        if self._check_if_file_exists():
            self._update_savings_file(game)
        else:
            self._create_savings_file(game)

    def _create_savings_file(self, game: Game) -> None:
        with open(self._file_path, 'w', encoding='utf-8') as savings_file:
            dump([game], savings_file)

    def _update_savings_file(self, game: Game) -> None:
        with open(self._file_path, 'r', encoding='utf-8') as savings_file:
            savings = load(savings_file)
            savings.insert(0, game)
        with open(self._file_path, 'w', encoding='utf-8') as savings_file:
            dump(savings, savings_file)

    def _check_if_file_exists(self) -> bool:
        return path.exists(self._file_path)

    def _handle_model_game_start(self, game: Game) -> None:
        self._save_game(game)

    def _handle_model_bet_make(self, game: Game) -> None:
        self._save_game(game)

    def _handle_card_issue(self, game: Game) -> None:
        self._save_game(game)

    def _handle_game_finish(self, game: Game) -> None:
        self._save_game(game)
