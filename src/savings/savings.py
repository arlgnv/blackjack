from typing import Any
import pathlib
import os
import json

from layers.model import model as model_layer, types as model_types


class Savings:
    _model: model_layer.Model
    _current_game_file_path: str
    _statistics_file_path: str

    def __init__(self, model: model_layer.Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._current_game_file_path = f'{pathlib.Path(__file__).parent}/current_game.json'
        self._statistics_file_path = f'{pathlib.Path(__file__).parent}/statistics.json'

    def load_current_game(self) -> model_types.Game | None:
        if os.path.exists(self._current_game_file_path):
            return self._read_file(self._current_game_file_path)

        return None

    def load_statistics(self) -> model_types.Statistics | None:
        if os.path.exists(self._statistics_file_path):
            return self._read_file(self._statistics_file_path)

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(model_types.EventNames.STATE_UPDATED.value,
                       self._handle_game_update)

    def _handle_game_update(self, state: model_types.State) -> None:
        game_stage = state['game']['stage']

        if game_stage not in (model_types.GameStages.FIRST_STARTING_IS_AWAITED.value, model_types.GameStages.STARTING_IS_AWAITED.value):
            if game_stage == model_types.GameStages.FINISHED.value:
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
