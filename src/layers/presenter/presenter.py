from observable import Observable
from layers.model import Game, EventNames as ModelEventNames
from layers.model.model import Model
from layers.view import EventNames as ViewEventNames
from layers.view.view import View

from .types import EventNames


class Presenter(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._model = Model()
        self._subscribe_to_model_events()

        self._view = View()
        self._subscribe_to_view_events()

    def start(self) -> None:
        self._view.update(self._model.get_game_state())

    def _subscribe_to_view_events(self) -> None:
        self._view.on(ViewEventNames.GAME_STARTED,
                      self._handle_view_game_start)
        self._view.on(ViewEventNames.BET_MADE, self._handle_view_bet_make)
        self._view.on(ViewEventNames.CARD_TAKEN, self._handle_card_take)
        self._view.on(ViewEventNames.CARD_REJECTED, self._handle_card_reject)
        self._view.on(ViewEventNames.GAME_RESTARTED,
                      self._handle_view_game_restart)

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.GAME_STARTED,
                       self._handle_model_game_started)
        self._model.on(ModelEventNames.BET_MADE, self._handle_model_bet_make)
        self._model.on(ModelEventNames.CARD_ISSUED, self._handle_card_issue)
        self._model.on(ModelEventNames.GAME_FINISHED, self._handle_game_finish)

    def _handle_view_game_start(self) -> None:
        self._model.start_game()

    def _handle_model_game_started(self, game: Game) -> None:
        self._view.update(game)

    def _handle_view_bet_make(self, amount: int) -> None:
        self._model.make_bet_for_player(amount)

    def _handle_model_bet_make(self, game: Game) -> None:
        self._view.update(game)

    def _handle_card_take(self) -> None:
        self._model.hand_out_card_to_player()

    def _handle_card_reject(self) -> None:
        self._model.finish_game()

    def _handle_card_issue(self, game: Game) -> None:
        self._view.update(game)

    def _handle_game_finish(self, game: Game) -> None:
        self.emit(EventNames.GAME_FINISHED, game)

        self._view.update(game)

    def _handle_view_game_restart(self) -> None:
        self._model.restart_game()
