from observable import EventNames

from ..model import Model, PlayerNames, MAX_CARDS_NUMBER_ON_HAND
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
        self._view.subscribe(EventNames.ENOUGH_SAID,
                             self._handle_enough_say)
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
        game_state = self._model.get_game_state()

        if game_state[PlayerNames.PLAYER.value]['is_full']:
            self._handle_game_finish()
        else:
            self._view.display_game_status(game_state)

    def _handle_enough_say(self) -> None:
        self._handle_game_finish()

    def _handle_game_finish(self) -> None:
        self._model.finish_game()
        self._view.display_game_status(self._model.get_game_state())

        self._model.restart_game()
        self._view.display_game_status(self._model.get_game_state())
