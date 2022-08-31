import random

from observable import Observable

from .types import Game, GameStages, PlayerNames, PlayerName
from .constants import DEFAULT_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND


class Model(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._game = DEFAULT_STATE

    def get_game_state(self) -> Game:
        return self._game

    def start_game(self) -> None:
        self._game['stage'] = GameStages.BET_IS_AWAITED

    def make_bet(self, amount: int) -> None:
        self._game['stage'] = GameStages.CARD_TAKING_IS_AWAITED
        self._game['bank'] = amount
        self._game[PlayerNames.PLAYER.value]['money'] -= amount

        self._hand_out_cards_to_skynet()
        self._hand_out_card(PlayerNames.PLAYER)
        self._hand_out_card(PlayerNames.PLAYER)

    def take_card(self) -> None:
        self._hand_out_card(PlayerNames.PLAYER)
        self._game[PlayerNames.PLAYER.value]['is_full'] = len(
            self._game[PlayerNames.PLAYER.value]['deck']) == MAX_CARDS_NUMBER_ON_HAND

    def finish_game(self) -> None:
        self._game['stage'] = GameStages.FINISHED

        winner = self._determine_winner()
        if winner:
            winnings = self._game['bank'] * 2

            self._game['winner'] = winner
            self._game['winnings'] = winnings
            self._game[winner.value]['money'] += winnings

    def restart_game(self) -> None:
        self._game['stage'] = GameStages.GAME_STARTING_IS_AWAITED
        self._game['deck'].extend(
            self._game[PlayerNames.SKYNET.value]['deck'])
        self._game['deck'].extend(
            self._game[PlayerNames.PLAYER.value]['deck'])
        self._game['bank'] = 0
        self._game['winner'] = None
        self._game['winnings'] = 0
        self._game[PlayerNames.SKYNET.value]['deck'].clear()
        self._game[PlayerNames.SKYNET.value]['score'] = 0
        self._game[PlayerNames.PLAYER.value]['deck'].clear()
        self._game[PlayerNames.PLAYER.value]['score'] = 0
        self._game[PlayerNames.PLAYER.value]['is_full'] = False

    def _hand_out_cards_to_skynet(self) -> None:
        self._hand_out_card(PlayerNames.SKYNET)
        self._hand_out_card(PlayerNames.SKYNET)

        while random.randint(0, 1) == 0 and len(self._game[PlayerNames.SKYNET.value]['deck']) < MAX_CARDS_NUMBER_ON_HAND and self._game[PlayerNames.SKYNET.value]['score'] < 20:
            self._hand_out_card(PlayerNames.SKYNET)

    def _hand_out_card(self, player_name: PlayerNames) -> None:
        card = self._game['deck'].pop(
            random.randrange(0, len(self._game['deck'])))

        self._game[player_name.value]['deck'].append(card)
        self._game[player_name.value]['score'] += card

    def _determine_winner(self) -> PlayerName | None:
        skynet_score = self._game[PlayerNames.SKYNET.value]['score']
        player_score = self._game[PlayerNames.PLAYER.value]['score']

        if skynet_score == player_score:
            return None

        return PlayerNames.SKYNET if abs(skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE) else PlayerNames.PLAYER
