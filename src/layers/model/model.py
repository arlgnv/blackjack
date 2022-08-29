import random

from layers.observable import Observable
from layers.model.constants import DEFAULT_STATE


class Model(Observable):
    def __init__(self):
        super().__init__()

        self._state = DEFAULT_STATE

    def get_state(self):
        return self._state

    def make_bet(self, amount):
        self._state['bank'] = amount
        self._state['player']['money'] -= amount

        self._hand_out_card('computer')
        self._hand_out_card('computer')
        self._hand_out_card('player')
        self._hand_out_card('player')

    def take_card(self):
        self._hand_out_card('player')

    def _hand_out_card(self, subject):
        card = self._state['deck'].pop(
            random.randint(0, len(self._state['deck']) - 1))
        self._state[subject]['deck'].append(card)
        self._state[subject]['score'] += card
