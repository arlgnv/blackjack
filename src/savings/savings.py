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

        self._game_file_path = f'{Path(__file__).parent}/game.json'
        self._does_game_file_exist = path.exists(
            self._game_file_path)

        self._statistics_file_path = f'{Path(__file__).parent}/statistics.json'
        self._does_statistics_file_exist = path.exists(
            self._statistics_file_path)

    def load_game(self) -> Game | None:
        if self._does_game_file_exist:
            return self._read_game_file()

        return None

    def load_statistics(self) -> Statistics | None:
        if self._does_statistics_file_exist:
            return self._read_statistics_file()

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.STATE_UPDATED, self._handle_game_update)

    def _handle_game_update(self, state: State) -> None:
        if state['game']['stage'] == GameStages.FINISHED.value:
            remove(self._game_file_path)
        else:
            self._write_to_game_file(state['game'])

        self._write_to_statistics_file(state['statistics'])

    def _write_to_game_file(self, content: Any) -> None:
        self._write_to_file(self._game_file_path, content)

    def _read_game_file(self) -> Any:
        return self._read_file(self._game_file_path)

    def _write_to_statistics_file(self, content: Any) -> None:
        self._write_to_file(self._statistics_file_path, content)

    def _read_statistics_file(self) -> Statistics:
        return self._read_file(self._statistics_file_path)

    def _write_to_file(self, file_path: str, content: Any) -> Any:
        with open(file_path, 'w', encoding='utf-8') as file:
            dump(content, file)

    def _read_file(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            return load(file)
