from observable import EventNames
from saver import Saver

from ..model import Model, GameStages
from ..view import View


class Presenter:
    def __init__(self) -> None:
        self._saver = Saver()
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
        self._view.subscribe(EventNames.CARD_REJECTED,
                             self._handle_card_reject)
        self._view.subscribe(EventNames.GAME_RESTARTED,
                             self._handle_game_restart)

    def _handle_game_start(self) -> None:
        self._model.start_game()
        self._view.display_game_status(self._model.get_game_state())

    def _handle_bet_make(self, amount: int) -> None:
        self._model.make_bet_for_player(amount)
        self._view.display_game_status(self._model.get_game_state())

    def _handle_card_take(self) -> None:
        self._model.hand_out_card_to_player()
        game_state = self._model.get_game_state()

        if game_state['stage'] == GameStages.FINISHED:
            self._saver.save_game(game_state)

        self._view.display_game_status(game_state)

    def _handle_card_reject(self) -> None:
        self._model.finish_game()
        game_state = self._model.get_game_state()
        self._saver.save_game(game_state)
        self._view.display_game_status(game_state)

    def _handle_game_restart(self) -> None:
        self._model.restart_game()
        self._view.display_game_status(self._model.get_game_state())
