from layers.view.view import View
from layers.view.types import EventNames as ViewEventNames
from layers.model.model import Model
from layers.model.types import State, EventNames as ModelEventNames


class Presenter():
    _view: View
    _model: Model

    def __init__(self, view: View, model: Model) -> None:
        self._view = view
        self._subscribe_to_view_events()

        self._model = model
        self._subscribe_to_model_events()

    def _subscribe_to_view_events(self) -> None:
        self._view.on(ViewEventNames.GAME_STARTED.value,
                      self._handle_game_start)
        self._view.on(ViewEventNames.MONEY_DEPOSITED.value,
                      self._handle_money_deposit)
        self._view.on(ViewEventNames.BET_MADE.value,
                      self._handle_bet_make)
        self._view.on(ViewEventNames.CARD_TAKEN.value,
                      self._handle_card_take)
        self._view.on(ViewEventNames.CARD_REJECTED.value,
                      self._handle_card_reject)
        self._view.on(ViewEventNames.GAME_RESTARTED.value,
                      self._handle_game_restart)

    def _handle_game_start(self) -> None:
        self._model.start_game()

    def _handle_money_deposit(self, amount: int) -> None:
        self._model.add_money_to_player(amount)

    def _handle_bet_make(self, amount: int) -> None:
        self._model.make_bet_for_player(amount)

    def _handle_card_take(self) -> None:
        self._model.issue_card_to_player()

    def _handle_card_reject(self) -> None:
        self._model.finish_game()

    def _handle_game_restart(self) -> None:
        self._model.restart_game()

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.STATE_UPDATED.value,
                       self._handle_state_update)

    def _handle_state_update(self, state: State) -> None:
        self._view.update(state)
