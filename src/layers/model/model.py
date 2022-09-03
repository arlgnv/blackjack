from random import choice, randrange

from observable import Observable

from .constants import DEFAULT_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND, SCORE_DESERVING_TAKING_RISK, SCORE_DONT_DESERVING_TAKING_RISK
from .types import Game, GameStages, PlayerNames, EventNames


class Model(Observable):
    def init_game(self, game: Game | None) -> None:
        self._game = game or DEFAULT_STATE

        self.emit(EventNames.GAME_STAGE_UPDATED, self._game)

    def start_game(self) -> None:
        self._game['stage'] = GameStages.DEPOSIT_IS_AWAITED if self._check_if_player_broke(
            PlayerNames.PLAYER) else GameStages.BET_IS_AWAITED
        self.emit(EventNames.GAME_STAGE_UPDATED, self._game)

    def add_money_to_player(self, amount: int) -> None:
        if amount:
            self._add_money(PlayerNames.PLAYER, amount)

        self._game['stage'] = GameStages.BET_IS_AWAITED
        self.emit(EventNames.GAME_STAGE_UPDATED, self._game)

    def make_bet_for_player(self, amount: int) -> None:
        if amount:
            self._game[PlayerNames.PLAYER.value]['money'] -= amount
            self._game['bank'] += amount * 2

        self._issue_cards_to_computer()
        self._issue_card(PlayerNames.PLAYER)
        self._issue_card(PlayerNames.PLAYER)

        self._game['stage'] = GameStages.CARD_TAKING_IS_AWAITED
        self.emit(EventNames.GAME_STAGE_UPDATED, self._game)

    def issue_card_to_player(self) -> None:
        self._issue_card(PlayerNames.PLAYER)

        if self._check_can_player_take_card(PlayerNames.PLAYER):
            self.emit(EventNames.GAME_STAGE_UPDATED, self._game)
        else:
            self.finish_game()

    def finish_game(self) -> None:
        winner = self._determine_winner()
        if winner:
            self._game['winner'] = winner
            self._game[winner.value]['wins'] += 1

        if self._game['bank']:
            self._distribute_winnings()

        self._game['stage'] = GameStages.FINISHED
        self.emit(EventNames.GAME_STAGE_UPDATED, self._game)

    def restart_game(self) -> None:
        self._game['winner'] = None

        self._take_cards_from_player(PlayerNames.COMPUTER)
        self._take_cards_from_player(PlayerNames.PLAYER)
        self.start_game()

    def _issue_cards_to_computer(self) -> None:
        self._issue_card(PlayerNames.COMPUTER)
        self._issue_card(PlayerNames.COMPUTER)

        while self._decide_whether_to_take_card_to_computer():
            self._issue_card(PlayerNames.COMPUTER)

    def _decide_whether_to_take_card_to_computer(self) -> bool:
        computer_score = self._game[PlayerNames.COMPUTER.value]['score']
        can_computer_take_card = self._check_can_player_take_card(
            PlayerNames.COMPUTER)
        is_it_stupid_to_take_a_card = computer_score > SCORE_DONT_DESERVING_TAKING_RISK
        if not can_computer_take_card or is_it_stupid_to_take_a_card:
            return False

        if computer_score < SCORE_DESERVING_TAKING_RISK:
            return True

        return choice((True, False))

    def _add_money(self, player_name: PlayerNames, amount: int) -> None:
        self._game[player_name.value]['money'] += amount

    def _issue_card(self, player_name: PlayerNames) -> None:
        card = self._game['deck'].pop(
            randrange(0, len(self._game['deck'])))

        self._game[player_name.value]['deck'].append(card)
        self._game[player_name.value]['score'] += card

    def _determine_winner(self) -> PlayerNames | None:
        skynet_score = self._game[PlayerNames.COMPUTER.value]['score']
        player_score = self._game[PlayerNames.PLAYER.value]['score']

        if skynet_score == player_score:
            return None

        return PlayerNames.COMPUTER if abs(skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE) else PlayerNames.PLAYER

    def _take_cards_from_player(self, player_name: PlayerNames) -> None:
        self._game['deck'].extend(
            self._game[player_name.value]['deck'])
        self._game[player_name.value]['deck'].clear()
        self._game[player_name.value]['score'] = 0

    def _distribute_winnings(self) -> None:
        bank = self._game['bank']
        winner = self._game['winner']

        if winner == PlayerNames.PLAYER:
            self._game[PlayerNames.PLAYER.value]['money'] += bank

        if not winner:
            self._game[PlayerNames.PLAYER.value]['money'] += int(bank / 2)

        self._game['bank'] = 0

    def _check_can_player_take_card(self, player_name: PlayerNames) -> bool:
        return len(
            self._game[player_name.value]['deck']) < MAX_CARDS_NUMBER_ON_HAND

    def _check_if_player_broke(self, player_name: PlayerNames) -> bool:
        return self._game[player_name.value]['money'] == 0
