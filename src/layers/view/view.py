from observable import Observable
from layers.model import Game, GameStages, PlayerNames

from .constants import WINNER_TO_DISPLAYED_WINNER, MESSAGES, AFFIRMATIVE_PLAYER_ANSWERS
from .types import EventNames


class View(Observable):
    def __init__(self) -> None:
        super().__init__()

        print(MESSAGES['welcome'])

    def update(self, game: Game) -> None:
        match game['stage']:
            case GameStages.STARTING_IS_AWAITED:
                self._request_game_starting()
            case GameStages.BET_IS_AWAITED:
                self._print_bet_preview(game)
                self._request_bet(game)
            case GameStages.CARD_TAKING_IS_AWAITED:
                self._print_player_result(game)
                self._request_card_taking()
            case GameStages.FINISHED:
                self._print_game_result(game)
                self._request_game_restart()
            case _:
                pass

    def _request_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input('Попытать удачу? [y/n] ')):
            self.emit(EventNames.GAME_STARTED)

    def _request_bet(self, game: Game) -> None:
        min_bet = game['bank']
        max_bet = game[PlayerNames.HUMAN.value]['money']

        while True:
            bet = input(f'Твоя ставка(мин. {min_bet}, макс. {max_bet}): ')

            if bet.isdigit():
                bet_as_int = int(bet)

                if min_bet <= bet_as_int <= max_bet:
                    break

        self.emit(EventNames.BET_MADE, bet_as_int)

    def _request_card_taking(self) -> None:
        if self._check_if_player_answer_affirmative(input('Возьмем еще карту? [y/n] ')):
            self.emit(EventNames.CARD_TAKEN)
        else:
            self.emit(EventNames.CARD_REJECTED)

    def _request_game_restart(self) -> None:
        if self._check_if_player_answer_affirmative(input('Сыграем еще разок? [y/n] ')):
            self.emit(EventNames.GAME_RESTARTED)

    def _check_if_player_answer_affirmative(self, answer: str) -> bool:
        return answer in AFFIRMATIVE_PLAYER_ANSWERS

    def _print_bet_preview(self, game: Game) -> None:
        print(f'''
===================
Банк: {game['bank']}
-------------------
Твои деньги: {game[PlayerNames.HUMAN.value]['money']}
===================
''')

    def _print_player_result(self, game: Game) -> None:
        print(f'''
===================
Банк: {game['bank']}
-------------------
Твои деньги: {game[PlayerNames.HUMAN.value]['money']}
Твои карты: {game[PlayerNames.HUMAN.value]['deck']}
Твои очки: {game[PlayerNames.HUMAN.value]['score']}
===================
''')

    def _print_game_result(self, game: Game) -> None:
        print(f'''
===================
Победитель: {WINNER_TO_DISPLAYED_WINNER[game['winner'].value] if game['winner'] else 'Ничья'}
-------------------
Твой результат:
  Карты - {game[PlayerNames.HUMAN.value]['deck']}
  Очки - {game[PlayerNames.HUMAN.value]['score']}
  Выигрышей за все время - {game[PlayerNames.HUMAN.value]['wins']}
-------------------
Результат Skynet:
  Карты - {game[PlayerNames.COMPUTER.value]['deck']}
  Очки - {game[PlayerNames.COMPUTER.value]['score']}
  Выигрышей за все время - {game[PlayerNames.COMPUTER.value]['wins']}
===================
''')
