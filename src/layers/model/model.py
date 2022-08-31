import random

from observable import Observable

from .types import Game, GameStages, PlayerNames
from .constants import DEFAULT_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND


class Model(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._game = DEFAULT_STATE

    def get_game_state(self) -> Game:
        return self._game

    def start_game(self) -> None:
        self._game['stage'] = GameStages.BET_IS_AWAITED

        self._make_bet_for_skynet()
        self._hand_out_cards_to_skynet()
        self.hand_out_card_to_player()
        self.hand_out_card_to_player()

    def make_bet_for_player(self, amount: int) -> None:
        self._game['stage'] = GameStages.CARD_TAKING_IS_AWAITED
        self._make_bet(PlayerNames.PLAYER, amount)

    def hand_out_card_to_player(self) -> None:
        self._hand_out_card(PlayerNames.PLAYER)

        if self._check_if_player_full(PlayerNames.PLAYER):
            self.finish_game()

    def finish_game(self) -> None:
        self._game['stage'] = GameStages.FINISHED
        self._game['winner'] = self._determine_winner()

    def restart_game(self) -> None:
        self._take_cards_from_player(PlayerNames.SKYNET)
        self._take_cards_from_player(PlayerNames.PLAYER)
        self._distribute_winnings()
        self.start_game()

    def _make_bet_for_skynet(self) -> None:
        self._make_bet(PlayerNames.SKYNET, random.randint(
            0, self._game[PlayerNames.SKYNET.value]['money']))

    def _hand_out_cards_to_skynet(self) -> None:
        self._hand_out_card(PlayerNames.SKYNET)
        self._hand_out_card(PlayerNames.SKYNET)

        while random.choice((True, False)) and not self._check_if_player_full(PlayerNames.SKYNET) and self._game[PlayerNames.SKYNET.value]['score'] < 20:
            self._hand_out_card(PlayerNames.SKYNET)

    def _make_bet(self, player_name: PlayerNames, amount: int) -> None:
        self._game[player_name.value]['money'] -= amount
        self._game['bank'] += amount

    def _hand_out_card(self, player_name: PlayerNames) -> None:
        card = self._game['deck'].pop(
            random.randrange(0, len(self._game['deck'])))

        self._game[player_name.value]['deck'].append(card)
        self._game[player_name.value]['score'] += card

    def _determine_winner(self) -> PlayerNames | None:
        skynet_score = self._game[PlayerNames.SKYNET.value]['score']
        player_score = self._game[PlayerNames.PLAYER.value]['score']

        if skynet_score == player_score:
            return None

        return PlayerNames.SKYNET if abs(skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE) else PlayerNames.PLAYER

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
        else:
            winnings = int(bank / 2)
            self._game[PlayerNames.SKYNET.value]['money'] += winnings
            self._game[PlayerNames.PLAYER.value]['money'] += winnings
        self._game['bank'] = 0
        self._game['winner'] = None

    def _check_if_player_full(self, player_name: PlayerNames) -> bool:
        return len(
            self._game[player_name.value]['deck']) == MAX_CARDS_NUMBER_ON_HAND
