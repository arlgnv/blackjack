from layers.model.model import Model
from layers.view.view import View


class Presenter:
    def __init__(self):
        self._model = Model()

        self._view = View(self._model.get_state())
        self._view.subscribe('betMade', self._make_bet)
        self._view.subscribe('cardTaken', self._take_card)
        self._view.subscribe('gameFinished', self._finish_game)

    def _make_bet(self, amount: int):
        self._model.make_bet(amount)
        self._view.display_status(self._model.get_state())

    def _take_card(self):
        self._model.take_card()
        self._view.display_status(self._model.get_state())

    def _finish_game(self):
        self._model.finish_game()
        self._view.display_status(self._model.get_state())
