import random

from observable import Observable

from .types import Game, GameStages, PlayerNames, PlayerName, Winner
from .constants import DEFAULT_STATE, WIN_SCORE, MAX_CARDS_NUMBER_ON_HAND, DRAW


class Model(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._game = DEFAULT_STATE

    def get_game_state(self) -> Game:
        return self._game

    def start_game(self) -> None:
        self._game['stage'] = GameStages.BET_IS_AWAITED.value

    def make_bet(self, amount: int) -> None:
        self._game['stage'] = GameStages.CARD_TAKING_IS_AWAITED.value
        self._game['bank'] = amount
        self._game[PlayerNames.PLAYER.value]['money'] -= amount

        self._hand_out_cards_to_skynet()
        self._hand_out_card(PlayerNames.PLAYER.value)
        self._hand_out_card(PlayerNames.PLAYER.value)

    def take_card(self) -> None:
        self._hand_out_card(PlayerNames.PLAYER.value)

        if len(self._game[PlayerNames.PLAYER.value]['deck']) == MAX_CARDS_NUMBER_ON_HAND:
            self.finish_game()

    def finish_game(self) -> None:
        self._game['stage'] = GameStages.FINISHED.value
        self._game['winner'] = self._get_winner()

    def reset_game_state(self) -> None:
        self._game['deck'].extend(
            self._game[PlayerNames.PLAYER.value]['deck'])
        self._game['deck'].extend(
            self._game[PlayerNames.SKYNET.value]['deck'])

        winner = self._game['winner']
        if winner and winner != DRAW:
            self._game[winner]['money'] += self._game['bank'] * 2
        self._game['winner'] = None

        self._game['bank'] = 0
        self._game[PlayerNames.PLAYER.value]['deck'].clear()
        self._game[PlayerNames.PLAYER.value]['score'] = 0
        self._game[PlayerNames.SKYNET.value]['deck'].clear()
        self._game[PlayerNames.SKYNET.value]['score'] = 0

    def _hand_out_cards_to_skynet(self) -> None:
        self._hand_out_card(PlayerNames.SKYNET.value)
        self._hand_out_card(PlayerNames.SKYNET.value)

        while random.randint(0, 1) == 0 and len(self._game[PlayerNames.SKYNET.value]['deck']) < MAX_CARDS_NUMBER_ON_HAND and self._game[PlayerNames.SKYNET.value]['score'] < 20:
            self._hand_out_card(PlayerNames.SKYNET.value)

    def _hand_out_card(self, player_name: PlayerName) -> None:
        card = self._game['deck'].pop(
            random.randrange(0, len(self._game['deck'])))

        self._game[player_name]['deck'].append(card)
        self._game[player_name]['score'] += card

    def _get_winner(self) -> Winner:
        skynet_score = self._game[PlayerNames.SKYNET.value]['score']
        player_score = self._game[PlayerNames.PLAYER.value]['score']

        if skynet_score == player_score:
            return DRAW

        return PlayerNames.SKYNET.value if abs(skynet_score - WIN_SCORE) < abs(player_score - WIN_SCORE) else PlayerNames.PLAYER.value
