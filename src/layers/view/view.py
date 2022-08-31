from observable import Observable, EventNames
from layers.model import Game, GameStages, PlayerNames

from .constants import WINNER_TO_DISPLAYED_WINNER, MESSAGES, AFFIRMATIVE_PLAYER_ANSWERS


class View(Observable):
    def __init__(self) -> None:
        super().__init__()

        self._print_welcome()

    def display_game_status(self, game: Game) -> None:
        match game['stage']:
            case GameStages.GAME_STARTING_IS_AWAITED:
                self._request_game_starting()
            case GameStages.BET_IS_AWAITED:
                self._request_bet(game)
            case GameStages.CARD_TAKING_IS_AWAITED:
                self._print_player_result(game)
                self._request_card_taking()
            case GameStages.FINISHED:
                self._print_game_result(game)
            case _:
                pass

    def _request_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input('Сыграем? [y/n] ')):
            self.notify(EventNames.GAME_STARTED)

    def _request_bet(self, game: Game) -> None:
        while True:
            bet = input(
                f'Твоя ставка(макс. {game[PlayerNames.PLAYER.value]["money"]}): ')

            if bet.isdigit():
                break

        self.notify(EventNames.BET_MADE, int(bet))

    def _request_card_taking(self) -> None:
        if self._check_if_player_answer_affirmative(input('Возьмем еще карту? [y/n] ')):
            self.notify(EventNames.CARD_TAKEN)
        else:
            self.notify(EventNames.CARD_REJECTED)

    def _check_if_player_answer_affirmative(self, answer: str) -> bool:
        return answer in AFFIRMATIVE_PLAYER_ANSWERS

    def _print_welcome(self) -> None:
        print(MESSAGES['welcome'])

    def _print_player_result(self, game: Game) -> None:
        print(f'''
Твои карты: {game[PlayerNames.PLAYER.value]['deck']}
Твои очки: {game[PlayerNames.PLAYER.value]['score']}
''')

    def _print_game_result(self, game: Game) -> None:
        print(f'''
Победитель: {WINNER_TO_DISPLAYED_WINNER[game['winner'].value] if game['winner'] else 'Ничья'}
===================
Твой результат:
  Карты - {game[PlayerNames.PLAYER.value]['deck']}
  Очки - {game[PlayerNames.PLAYER.value]['score']}
===================
Результат Skynet:
  Карты - {game[PlayerNames.SKYNET.value]['deck']}
  Очки - {game[PlayerNames.SKYNET.value]['score']}
''')
