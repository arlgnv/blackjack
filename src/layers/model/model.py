import copy
import random

from observable import observable

from . import constants, types


class Model(observable.Observable):
    _state: types.State

    def __init__(self) -> None:
        super().__init__()

        self._state = copy.deepcopy(constants.INITIAL_STATE)

    def get_state(self) -> types.State:
        return self._state

    def set_state(self, state: types.State) -> None:
        self._state = state

        self._emit(types.EventNames.STATE_UPDATED.value, self._state)

    def start_game(self) -> None:
        if self._state['game']['stage'] == types.GameStages.FINISHED.value:
            if self._state['game']['winner']:
                self._state['game']['winner'] = None

            self._take_cards_from_player(types.PlayerNames.COMPUTER.value)
            self._take_cards_from_player(types.PlayerNames.PLAYER.value)

        is_player_broke = self._state['statistics']['player']['money'] == 0
        self._state['game']['stage'] = types.GameStages.DEPOSIT_IS_AWAITED.value if is_player_broke else types.GameStages.BET_IS_AWAITED.value

        self._emit(types.EventNames.STATE_UPDATED.value, self._state)

    def add_money_to_player(self, amount: int) -> None:
        if amount:
            self._state['statistics']['player']['money'] += amount
            self._state['game']['stage'] = types.GameStages.BET_IS_AWAITED.value
        else:
            self._make_first_hand()
            self._state['game']['stage'] = types.GameStages.CARD_TAKING_IS_AWAITED.value

        self._emit(types.EventNames.STATE_UPDATED.value, self._state)

    def make_bet_for_player(self, amount: int) -> None:
        if amount:
            self._state['statistics']['player']['money'] -= amount
            self._state['game']['bank'] = amount * 2

        self._make_first_hand()
        self._state['game']['stage'] = types.GameStages.CARD_TAKING_IS_AWAITED.value
        self._emit(types.EventNames.STATE_UPDATED.value, self._state)

    def issue_card_to_player(self) -> None:
        self._issue_card(types.PlayerNames.PLAYER.value)

        if self._check_can_player_take_card(types.PlayerNames.PLAYER.value):
            self._emit(types.EventNames.STATE_UPDATED.value, self._state)
        else:
            self.finish_game()

    def finish_game(self) -> None:
        winner = self._determine_winner()
        if winner:
            self._state['game']['winner'] = winner
            self._state['statistics'][winner]['wins'] += 1

        if self._state['game']['bank']:
            self._distribute_winnings()

        self._state['game']['stage'] = types.GameStages.FINISHED.value
        self._emit(types.EventNames.STATE_UPDATED.value, self._state)

    def _make_first_hand(self) -> None:
        self._issue_cards_to_computer()
        self._issue_card(types.PlayerNames.PLAYER.value)
        self._issue_card(types.PlayerNames.PLAYER.value)

    def _issue_cards_to_computer(self) -> None:
        self._issue_card(types.PlayerNames.COMPUTER.value)
        self._issue_card(types.PlayerNames.COMPUTER.value)

        while self._check_can_player_take_card(types.PlayerNames.COMPUTER.value) and self._decide_whether_to_take_card_to_computer():
            self._issue_card(types.PlayerNames.COMPUTER.value)

    def _decide_whether_to_take_card_to_computer(self) -> bool:
        computer_score = self._state['game']['computer']['score']

        if computer_score > 20:
            return False

        if computer_score < 17:
            return True

        return random.choice((True, False))

    def _issue_card(self, player_name: types.PlayerName) -> None:
        card = self._state['game']['deck'].pop(
            random.randrange(0, len(self._state['game']['deck'])))

        self._state['game'][player_name]['deck'].append(card)
        self._state['game'][player_name]['score'] += card

    def _determine_winner(self) -> types.PlayerName | None:
        skynet_score = self._state['game']['computer']['score']
        player_score = self._state['game']['player']['score']

        if skynet_score == player_score:
            return None

        is_computer_score_closer_to_win_score = abs(
            skynet_score - constants.WIN_SCORE) < abs(player_score - constants.WIN_SCORE)

        return types.PlayerNames.COMPUTER.value if is_computer_score_closer_to_win_score else types.PlayerNames.PLAYER.value

    def _take_cards_from_player(self, player_name: types.PlayerName) -> None:
        self._state['game']['deck'].extend(
            self._state['game'][player_name]['deck'])
        self._state['game'][player_name]['deck'].clear()
        self._state['game'][player_name]['score'] = 0

    def _distribute_winnings(self) -> None:
        bank = self._state['game']['bank']
        winner = self._state['game']['winner']

        if winner == types.PlayerNames.PLAYER.value:
            self._state['statistics']['player']['money'] += bank

        if not winner:
            self._state['statistics']['player']['money'] += int(
                bank / 2)

        self._state['game']['bank'] = 0

    def _check_can_player_take_card(self, player_name: types.PlayerName) -> bool:
        return len(
            self._state['game'][player_name]['deck']) < constants.MAX_CARDS_NUMBER_ON_HAND
