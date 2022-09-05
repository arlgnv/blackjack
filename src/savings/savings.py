from typing import Any
from pathlib import Path
from os import path, remove
from json import load, dump

from layers.model import State, Game, GameStages, Statistics, EventNames as ModelEventNames
from layers.model.model import Model


class Savings:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._current_game_file_path = f'{Path(__file__).parent}/current_game.json'
        self._statistics_file_path = f'{Path(__file__).parent}/statistics.json'

    def load_current_game(self) -> Game | None:
        if path.exists(self._current_game_file_path):
            return self._read_file(self._current_game_file_path)

        return None

    def load_statistics(self) -> Statistics | None:
        if path.exists(self._statistics_file_path):
            return self._read_file(self._statistics_file_path)

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.STATE_UPDATED, self._handle_game_update)

    def _handle_game_update(self, state: State) -> None:
        game_stage = state['game']['stage']

        if game_stage not in (GameStages.FIRST_STARTING_IS_AWAITED.value, GameStages.STARTING_IS_AWAITED.value):
            if game_stage == GameStages.FINISHED.value:
                remove(self._current_game_file_path)
            else:
                self._write_to_file(
                    self._current_game_file_path, state['game'])

            self._write_to_file(self._statistics_file_path,
                                state['statistics'])

    def _write_to_file(self, file_path: str, content: Any) -> Any:
        with open(file_path, 'w', encoding='utf-8') as file:
            dump(content, file)

    def _read_file(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            return load(file)
