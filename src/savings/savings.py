from pathlib import Path
from os import path
from json import load, dump

from layers.model import Game, GameStages, PlayerNames, EventNames as ModelEventNames
from layers.model.model import Model


class Savings:
    def __init__(self, model: Model) -> None:
        self._model = model
        self._subscribe_to_model_events()

        self._savings_file_path = f'{Path(__file__).parent}/savings.json'
        self._is_savings_file_exists = self._check_if_savings_file_exists()

    def load_last_saving(self) -> Game | None:
        if self._is_savings_file_exists:
            with open(self._savings_file_path, 'r', encoding='utf-8') as savings_file:
                last_saving = load(savings_file)[0]
                last_saving['stage'] = GameStages(last_saving['stage'])

                winner = last_saving['winner']
                if winner:
                    last_saving['winner'] = PlayerNames(winner)
                print(last_saving)
                return last_saving

        return None

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.GAME_STARTED,
                       self._handle_model_game_start)
        self._model.on(ModelEventNames.BET_MADE, self._handle_model_bet_make)
        self._model.on(ModelEventNames.CARD_ISSUED, self._handle_card_issue)
        self._model.on(ModelEventNames.GAME_FINISHED, self._handle_game_finish)

    def _save_game(self, game: Game) -> None:
        if self._is_savings_file_exists:
            self._update_last_saving(game)
        else:
            self._create_savings_file(game)

    def _create_savings_file(self, game: Game) -> None:
        with open(self._savings_file_path, 'w', encoding='utf-8') as savings_file:
            dump([game], savings_file)

        self._is_savings_file_exists = True

    def _add_saving(self, game: Game) -> None:
        with open(self._savings_file_path, 'r', encoding='utf-8') as savings_file:
            savings = load(savings_file)
            savings.insert(0, game)
        with open(self._savings_file_path, 'w', encoding='utf-8') as savings_file:
            dump(savings, savings_file)

    def _update_last_saving(self, game: Game) -> None:
        with open(self._savings_file_path, 'r', encoding='utf-8') as savings_file:
            savings = load(savings_file)
            savings[0] = game
        with open(self._savings_file_path, 'w', encoding='utf-8') as savings_file:
            dump(savings, savings_file)

    def _check_if_savings_file_exists(self) -> bool:
        return path.exists(self._savings_file_path)

    def _handle_model_game_start(self, game: Game) -> None:
        if self._is_savings_file_exists:
            self._add_saving(game)
        else:
            self._create_savings_file(game)

    def _handle_model_bet_make(self, game: Game) -> None:
        if self._is_savings_file_exists:
            self._update_last_saving(game)
        else:
            self._create_savings_file(game)

    def _handle_card_issue(self, game: Game) -> None:
        if self._is_savings_file_exists:
            self._update_last_saving(game)
        else:
            self._create_savings_file(game)

    def _handle_game_finish(self, game: Game) -> None:
        if self._is_savings_file_exists:
            self._update_last_saving(game)
        else:
            self._create_savings_file(game)
