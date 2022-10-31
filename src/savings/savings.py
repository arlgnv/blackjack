from typing import Any
import os
import json

from layers.model.types import State

from .constants import SAVINGS_FILE_PATH


class Savings:
    _is_savings_file_exist: bool

    def __init__(self) -> None:
        self._is_savings_file_exist = os.path.exists(SAVINGS_FILE_PATH)

    def load(self) -> State | None:
        if self._is_savings_file_exist:
            return self._read_file(SAVINGS_FILE_PATH)

        return None

    def save(self, state: State) -> None:
        self._write_to_file(SAVINGS_FILE_PATH, state)

    def _write_to_file(self, file_path: str, content: Any) -> Any:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(content, file)

    def _read_file(self, file_path: str) -> Any:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
