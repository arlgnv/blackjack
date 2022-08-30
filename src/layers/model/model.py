import random

from observable.observable import Observable

from layers.model.constants import DEFAULT_STATE
from layers.model.types import Subject


class Model(Observable):
    def __init__(self):
        super().__init__()

        self._state = DEFAULT_STATE

    def get_state(self):
        return self._state

    def make_bet(self, amount: int):
        self._state['bank'] = amount
        self._state['player']['money'] -= amount

        self._hand_out_to_skynet()
        self._hand_out_card('player')
        self._hand_out_card('player')

    def take_card(self):
        self._hand_out_card('player')

    def _hand_out_to_skynet(self):
        self._hand_out_card('skynet')
        self._hand_out_card('skynet')

        while random.randint(0, 1) == 0 and len(self._state['skynet']['deck']) < 5 and self._state['skynet']['score'] < 21:
            self._hand_out_card('skynet')

    def _hand_out_card(self, subject: Subject):
        card = self._state['deck'].pop(
            random.randint(0, len(self._state['deck']) - 1))
        self._state[subject]['deck'].append(card)
        self._state[subject]['score'] += card
