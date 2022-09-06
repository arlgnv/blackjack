from layers.view import view as view_layer, types as view_types
from layers.model import model as model_layer, types as model_types


class Presenter():
    _view: view_layer.View
    _model: model_layer.Model

    def __init__(self, view: view_layer.View, model: model_layer.Model) -> None:
        self._view = view
        self._subscribe_to_view_events()

        self._model = model
        self._subscribe_to_model_events()

    def _subscribe_to_view_events(self) -> None:
        self._view.on(view_types.EventNames.GAME_STARTED.value,
                      self._handle_game_start)
        self._view.on(view_types.EventNames.MONEY_DEPOSITED.value,
                      self._handle_money_deposit)
        self._view.on(view_types.EventNames.BET_MADE.value,
                      self._handle_bet_make)
        self._view.on(view_types.EventNames.CARD_TAKEN.value,
                      self._handle_card_take)
        self._view.on(view_types.EventNames.CARD_REJECTED.value,
                      self._handle_card_reject)
        self._view.on(view_types.EventNames.GAME_RESTARTED.value,
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
        self._model.start_game()

    def _subscribe_to_model_events(self) -> None:
        self._model.on(model_types.EventNames.STATE_UPDATED.value,
                       self._handle_game_update)

    def _handle_game_update(self, state: model_types.State) -> None:
        self._view.update(state)
