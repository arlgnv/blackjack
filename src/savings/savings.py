from typing import Any
from pathlib import Path
from os import path
from json import load, dump

from layers.model import Game, GameStages, PlayerNames, EventNames as ModelEventNames
from layers.model.model import Model


class Savings:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._savings_path = f'{Path(__file__).parent}/savings.json'
        self._is_savings_exists = path.exists(self._savings_path)

    def load_last_saving(self) -> Game | None:
        if self._is_savings_exists:
            with open(self._savings_path, 'r', encoding='utf-8') as savings_file:
                last_saving = load(savings_file)[0]
                last_saving['stage'] = GameStages(last_saving['stage'])

                winner = last_saving['winner']
                if winner:
                    last_saving['winner'] = PlayerNames(winner)

                return last_saving

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.GAME_STARTED,
                       self._save_game)
        self._model.on(ModelEventNames.BET_MADE, self._save_game)
        self._model.on(ModelEventNames.CARD_ISSUED, self._save_game)
        self._model.on(ModelEventNames.GAME_FINISHED, self._save_game)

    def _save_game(self, game: Game) -> None:
        if self._is_savings_exists:
            if game['stage'] == GameStages.FINISHED:
                self._add_saving(game)
            else:
                self._update_last_saving(game)
        else:
            self._write_to_savings_file([game])
            self._is_savings_exists = True

    def _write_to_savings_file(self, content: Any) -> None:
        with open(self._savings_path, 'w', encoding='utf-8') as savings_file:
            dump(content, savings_file)

    def _add_saving(self, game: Game) -> None:
        with open(self._savings_path, 'r', encoding='utf-8') as savings_file:
            savings = load(savings_file)
            savings.insert(0, game)
        self._write_to_savings_file(savings)

    def _update_last_saving(self, game: Game) -> None:
        with open(self._savings_path, 'r', encoding='utf-8') as savings_file:
            savings = load(savings_file)
            savings[0] = game
        self._write_to_savings_file(savings)
