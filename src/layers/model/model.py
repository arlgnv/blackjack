from typing import Any
from random import choice, randrange

from observable import Observable

from .constants import INITIAL_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND, SCORE_WORTH_RISK, SCORE_NOT_WORTH_RISK
from .types import State, GameStages,  PlayerNames, EventNames


class Model(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._state = INITIAL_STATE

    def get_state(self) -> State:
        return self._state

    def update_game(self, game: Any) -> None:
        self._state['game'] = {**self._state['game'], **game}

    def update_statistics(self, statistics: Any) -> None:
        self._state['statistics'] = {**self._state['statistics'], **statistics}

    def start_game(self) -> None:
        is_player_broke = self._state['statistics'][PlayerNames.PLAYER.value]['money'] == 0

        self._state['game']['stage'] = GameStages.DEPOSIT_IS_AWAITED if is_player_broke else GameStages.BET_IS_AWAITED
        self.emit(EventNames.STATE_UPDATED, self._state)

    def add_money_to_player(self, amount: int) -> None:
        if amount:
            self._state['statistics'][PlayerNames.PLAYER.value]['money'] += amount
            self._state['game']['stage'] = GameStages.BET_IS_AWAITED
        else:
            self._make_first_hand()
            self._state['game']['stage'] = GameStages.CARD_TAKING_IS_AWAITED

        self.emit(EventNames.STATE_UPDATED, self._state)

    def make_bet_for_player(self, amount: int) -> None:
        if amount:
            self._state['statistics'][PlayerNames.PLAYER.value]['money'] -= amount
            self._state['game']['bank'] = amount * 2

        self._make_first_hand()
        self._state['game']['stage'] = GameStages.CARD_TAKING_IS_AWAITED
        self.emit(EventNames.STATE_UPDATED, self._state)

    def issue_card_to_player(self) -> None:
        self._issue_card(PlayerNames.PLAYER)

        if self._check_can_player_take_card(PlayerNames.PLAYER):
            self.emit(EventNames.STATE_UPDATED, self._state)
        else:
            self.finish_game()

    def finish_game(self) -> None:
        winner = self._determine_winner()
        if winner:
            self._state['game']['winner'] = winner
            self._state['statistics'][winner.value]['wins'] += 1

        if self._state['game']['bank']:
            self._distribute_winnings()

        self._state['game']['stage'] = GameStages.FINISHED
        self.emit(EventNames.STATE_UPDATED, self._state)

    def restart_game(self) -> None:
        self._state['game']['winner'] = None
        self._take_cards_from_player(PlayerNames.COMPUTER)
        self._take_cards_from_player(PlayerNames.PLAYER)
        self.start_game()

    def _make_first_hand(self) -> None:
        self._issue_cards_to_computer()
        self._issue_card(PlayerNames.PLAYER)
        self._issue_card(PlayerNames.PLAYER)

    def _issue_cards_to_computer(self) -> None:
        self._issue_card(PlayerNames.COMPUTER)
        self._issue_card(PlayerNames.COMPUTER)

        while self._decide_whether_to_take_card_to_computer():
            self._issue_card(PlayerNames.COMPUTER)

    def _decide_whether_to_take_card_to_computer(self) -> bool:
        computer_score = self._state['game'][PlayerNames.COMPUTER.value]['score']
        is_it_stupid_to_take_card = computer_score > SCORE_NOT_WORTH_RISK
        can_computer_take_card = self._check_can_player_take_card(
            PlayerNames.COMPUTER)

        if is_it_stupid_to_take_card or not can_computer_take_card:
            return False

        if computer_score < SCORE_WORTH_RISK:
            return True

        return choice((True, False))

    def _issue_card(self, player_name: PlayerNames) -> None:
        card = self._state['game']['deck'].pop(
            randrange(0, len(self._state['game']['deck'])))

        self._state['game'][player_name.value]['deck'].append(card)
        self._state['game'][player_name.value]['score'] += card

    def _determine_winner(self) -> PlayerNames | None:
        skynet_score = self._state['game'][PlayerNames.COMPUTER.value]['score']
        player_score = self._state['game'][PlayerNames.PLAYER.value]['score']

        if skynet_score == player_score:
            return None

        is_computer_score_closer_to_win_score = abs(
            skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE)

        return PlayerNames.COMPUTER if is_computer_score_closer_to_win_score else PlayerNames.PLAYER

    def _take_cards_from_player(self, player_name: PlayerNames) -> None:
        self._state['game']['deck'].extend(
            self._state['game'][player_name.value]['deck'])
        self._state['game'][player_name.value]['deck'].clear()
        self._state['game'][player_name.value]['score'] = 0

    def _distribute_winnings(self) -> None:
        bank = self._state['game']['bank']
        winner = self._state['game']['winner']

        if winner == PlayerNames.PLAYER:
            self._state['statistics'][PlayerNames.PLAYER.value]['money'] += bank

        if not winner:
            self._state['statistics'][PlayerNames.PLAYER.value]['money'] += int(
                bank / 2)

        self._state['game']['bank'] = 0

    def _check_can_player_take_card(self, player_name: PlayerNames) -> bool:
        return len(
            self._state['game'][player_name.value]['deck']) < MAX_CARDS_NUMBER_ON_HAND
