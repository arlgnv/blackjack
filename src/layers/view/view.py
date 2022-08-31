from observable import Observable, EventNames
from layers.model import Game, GameStages, PlayerNames

from .constants import WINNER_TO_DISPLAYED_WINNER, MESSAGES


class View(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._print_welcome()

    def display_game_status(self, game: Game) -> None:
        match game['stage']:
            case GameStages.GAME_STARTING_IS_AWAITED.value:
                self._request_game_starting()
            case GameStages.BET_IS_AWAITED.value:
                self._request_bet(game)
            case GameStages.CARD_TAKING_IS_AWAITED.value:
                self._print_player_result(game)
                self._request_card_taking()
            case GameStages.FINISHED.value:
                self._print_game_result(game)
            case _:
                pass

    def _request_game_starting(self) -> None:
        if self._check_if_player_response_affirmative(input('Сыграем? [y/n] ').lower()):
            self.notify(EventNames.GAME_STARTED.value)

    def _request_bet(self, game: Game) -> None:
        self.notify(EventNames.BET_MADE.value, int(
            input(f'Твоя ставка(макс. {game["player"]["money"]}): ')))

    def _request_card_taking(self) -> None:
        if self._check_if_player_response_affirmative(input('Возьмем еще карту? [y/n] ').lower()):
            self.notify(EventNames.CARD_TAKEN.value)
        else:
            self.notify(EventNames.GAME_FINISHED.value)

    def _check_if_player_response_affirmative(self, response: str) -> bool:
        return response in ('', 'y')

    def _print_welcome(self) -> None:
        print(MESSAGES['welcome'])

    def _print_player_result(self, game: Game) -> None:
        print(f'''
Твои карты: {game[PlayerNames.PLAYER.value]['deck']}
Твои очки: {game[PlayerNames.PLAYER.value]['score']}
''')

    def _print_game_result(self, game: Game) -> None:
        print(f'''
Победитель: {WINNER_TO_DISPLAYED_WINNER[game['winner']] if game['winner'] else 'Ничья'}
===============
Твои карты: {game[PlayerNames.PLAYER.value]['deck']}
Твои очки: {game[PlayerNames.PLAYER.value]['score']}
===============
Карты компьютера: {game[PlayerNames.SKYNET.value]['deck']}
Очки компьютера: {game[PlayerNames.SKYNET.value]['score']}
''')
