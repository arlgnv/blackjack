import random

from observable.observable import Observable

from layers.model.constants import DEFAULT_STATE, WIN_SCORE, COMPUTER_NAME
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

        self._hand_out_cards_to_skynet()
        self._hand_out_card('player')
        self._hand_out_card('player')

    def take_card(self):
        self._hand_out_card('player')

        if len(self._state['player']['deck']) == 5:
            self.finish_game()

    def finish_game(self):
        winner = self._get_winner(
            self._state['player']['score'], self._state[COMPUTER_NAME]['score'])
        self._state['is_finished'] = True
        self._state['deck'].extend(
            self._state['player']['deck'])
        self._state['deck'].extend(
            self._state[COMPUTER_NAME]['deck'])
        self._state['winner'] = winner
        self._state[winner]['money'] += self._state['bank'] * 2
        self._state['bank'] = 0
        self._state['player']['deck'].clear()
        self._state['player']['score'] = 0
        self._state[COMPUTER_NAME]['deck'].clear()
        self._state[COMPUTER_NAME]['score'] = 0

    def _hand_out_cards_to_skynet(self):
        self._hand_out_card(COMPUTER_NAME)
        self._hand_out_card(COMPUTER_NAME)

        while random.randint(0, 1) == 0 and len(self._state[COMPUTER_NAME]['deck']) < 5 and self._state[COMPUTER_NAME]['score'] < 20:
            self._hand_out_card(COMPUTER_NAME)

    def _hand_out_card(self, subject: Subject):
        card = self._state['deck'].pop(
            random.randint(0, len(self._state['deck']) - 1))
        self._state[subject]['deck'].append(card)
        self._state[subject]['score'] += card

    def _get_winner(self, player_score: int, skynet_score: int):
        return 'player' if abs(player_score - WIN_SCORE) < abs(skynet_score - WIN_SCORE) else COMPUTER_NAME
