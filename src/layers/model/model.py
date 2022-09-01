from random import randint, choice, randrange

from observable import Observable

from .constants import DEFAULT_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND
from .types import Game, GameStages, PlayerNames


class Model(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._game = DEFAULT_STATE

    def get_game_state(self) -> Game:
        return self._game

    def start_game(self) -> None:
        self._game['stage'] = GameStages.BET_IS_AWAITED

        self._make_bet_for_computer()
        self._hand_out_cards_to_computer()
        self.hand_out_card_to_player()
        self.hand_out_card_to_player()

    def make_bet_for_player(self, amount: int) -> None:
        self._game['stage'] = GameStages.CARD_TAKING_IS_AWAITED
        self._make_bet(PlayerNames.HUMAN, amount)

    def hand_out_card_to_player(self) -> None:
        self._hand_out_card(PlayerNames.HUMAN)

        if self._check_can_player_take_card(PlayerNames.HUMAN):
            self.finish_game()

    def finish_game(self) -> None:
        self._game['stage'] = GameStages.FINISHED
        self._game['winner'] = self._determine_winner()

    def restart_game(self) -> None:
        self._take_cards_from_player(PlayerNames.COMPUTER)
        self._take_cards_from_player(PlayerNames.HUMAN)
        self._distribute_winnings()
        self.start_game()

    def _make_bet_for_computer(self) -> None:
        min_bet = 0
        max_bet = min([self._game[PlayerNames.COMPUTER.value]
                      ['money'], self._game[PlayerNames.HUMAN.value]['money']])

        self._make_bet(PlayerNames.COMPUTER, randint(min_bet, max_bet))

    def _hand_out_cards_to_computer(self) -> None:
        self._hand_out_card(PlayerNames.COMPUTER)
        self._hand_out_card(PlayerNames.COMPUTER)

        while self._decide_whether_to_take_card_to_computer():
            self._hand_out_card(PlayerNames.COMPUTER)

    def _decide_whether_to_take_card_to_computer(self) -> bool:
        computer_score = self._game[PlayerNames.COMPUTER.value]['score']
        can_computer_take_card = self._check_can_player_take_card(
            PlayerNames.COMPUTER)
        is_it_stupid_to_take_a_card = computer_score > 19
        if not can_computer_take_card or is_it_stupid_to_take_a_card:
            return False

        if computer_score < 16:
            return True

        return choice((True, False))

    def _make_bet(self, player_name: PlayerNames, amount: int) -> None:
        self._game[player_name.value]['money'] -= amount
        self._game['bank'] += amount

    def _hand_out_card(self, player_name: PlayerNames) -> None:
        card = self._game['deck'].pop(
            randrange(0, len(self._game['deck'])))

        self._game[player_name.value]['deck'].append(card)
        self._game[player_name.value]['score'] += card

    def _determine_winner(self) -> PlayerNames | None:
        skynet_score = self._game[PlayerNames.COMPUTER.value]['score']
        player_score = self._game[PlayerNames.HUMAN.value]['score']

        if skynet_score == player_score:
            return None

        return PlayerNames.COMPUTER if abs(skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE) else PlayerNames.HUMAN

    def _take_cards_from_player(self, player_name: PlayerNames) -> None:
        self._game['deck'].extend(
            self._game[player_name.value]['deck'])
        self._game[player_name.value]['deck'].clear()
        self._game[player_name.value]['score'] = 0

    def _distribute_winnings(self) -> None:
        bank = self._game['bank']
        winner = self._game['winner']

        if winner:
            self._game[winner.value]['money'] += bank
            self._game['winner'] = None
        else:
            winnings = int(bank / 2)
            self._game[PlayerNames.COMPUTER.value]['money'] += winnings
            self._game[PlayerNames.HUMAN.value]['money'] += winnings

        self._game['bank'] = 0

    def _check_can_player_take_card(self, player_name: PlayerNames) -> bool:
        return len(
            self._game[player_name.value]['deck']) < MAX_CARDS_NUMBER_ON_HAND
