from layers.model.model import Model
from layers.view.view import View


class Presenter:
    def __init__(self):
        self._model = Model()
        self._view = View()

        self._view.subscribe('betMade', self._make_bet)
        self._view.subscribe('cardTaken', self._take_card)
        self._view.request_bet(self._model.get_state())

    def _make_bet(self, amount: int):
        self._model.make_bet(amount)
        self._view.display_status(self._model.get_state())
        self._view.request_card_taking()

    def _take_card(self):
        self._model.take_card()
        state = self._model.get_state()

        self._view.display_status(state)

        if len(state['player']['deck']) < 5:
            self._view.request_card_taking()
        else:
            print('Игра окончена')
