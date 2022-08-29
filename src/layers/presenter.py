from layers.model.model import Model
from layers.view.view import View


class Presenter:
    def __init__(self):
        self._model = Model()
        self._view = View()

        self._view.subscribe('betMade', self._make_bet)
        self._view.subscribe('cardTaken', self._take_card)
        self._view.request_bet(self._model.get_state())

    def _make_bet(self, amount):
        self._model.make_bet(amount)
        self._view.display_status(self._model.get_state())
        self._view.request_action()

    def _take_card(self):
        self._model.take_card()
        self._view.display_status(self._model.get_state())
