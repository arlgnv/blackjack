from typing import Any
import pathlib
import os
import json

import layers.model.types as ModelTypes
from layers.model import model


class Savings:
    def __init__(self, model: model.Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._current_game_file_path = f'{pathlib.Path(__file__).parent}/current_game.json'
        self._statistics_file_path = f'{pathlib.Path(__file__).parent}/statistics.json'

    def load_current_game(self) -> ModelTypes.Game | None:
        if os.path.exists(self._current_game_file_path):
            return self._read_file(self._current_game_file_path)

        return None

    def load_statistics(self) -> ModelTypes.Statistics | None:
        if os.path.exists(self._statistics_file_path):
            return self._read_file(self._statistics_file_path)

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelTypes.EventNames.STATE_UPDATED,
                       self._handle_game_update)

    def _handle_game_update(self, state: ModelTypes.State) -> None:
        game_stage = state['game']['stage']

        if game_stage not in (ModelTypes.GameStages.FIRST_STARTING_IS_AWAITED.value, ModelTypes.GameStages.STARTING_IS_AWAITED.value):
            if game_stage == ModelTypes.GameStages.FINISHED.value:
                os.remove(self._current_game_file_path)
            else:
                self._write_to_file(
                    self._current_game_file_path, state['game'])

            self._write_to_file(self._statistics_file_path,
                                state['statistics'])

    def _write_to_file(self, file_path: str, content: Any) -> Any:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file)

    def _read_file(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
