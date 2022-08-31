from observable import EventNames

from ..model import Model
from ..view import View


class Presenter:
    def __init__(self) -> None:
        self._model = Model()
        self._view = View()
        self._subscribe_to_view_events()
        self._view.display_game_status(self._model.get_game_state())

    def _subscribe_to_view_events(self) -> None:
        self._view.subscribe(EventNames.GAME_STARTED,
                             self._handle_game_start)
        self._view.subscribe(EventNames.BET_MADE, self._handle_bet_make)
        self._view.subscribe(EventNames.CARD_TAKEN,
                             self._handle_card_take)
        self._view.subscribe(EventNames.GAME_FINISHED,
                             self._handle_game_finish)

    def _handle_game_start(self) -> None:
        self._model.start_game()
        self._view.display_game_status(self._model.get_game_state())

    def _handle_bet_make(self, amount: int) -> None:
        self._model.make_bet(amount)
        self._view.display_game_status(self._model.get_game_state())

    def _handle_card_take(self) -> None:
        self._model.take_card()
        self._view.display_game_status(self._model.get_game_state())

    def _handle_game_finish(self) -> None:
        self._model.finish_game()
        self._view.display_game_status(self._model.get_game_state())
        self._model.restart_game()
        self._view.display_game_status(self._model.get_game_state())
