from typing import Any
import pathlib
import os
import json

from layers.model import types as model_types


class Savings:
    _saving_file_path: str

    def __init__(self) -> None:
        self._saving_file_path = f'{pathlib.Path(__file__).parent}/saving.json'

    def load(self) -> model_types.State | None:
        if os.path.exists(self._saving_file_path):
            return self._read_file(self._saving_file_path)

        return None

    def save(self, state: model_types.State) -> None:
        self._write_to_file(self._saving_file_path, state)

    def _write_to_file(self, file_path: str, content: Any) -> Any:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file)

    def _read_file(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
