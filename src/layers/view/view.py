from observable import Observable
from layers.model import State, GameStages, MIN_BET

from .constants import WINNER_TO_DISPLAYED_WINNER, MESSAGES, AFFIRMATIVE_PLAYER_ANSWERS, RUBLE_SIGN
from .types import EventNames


class View(Observable):
    def update(self, state: State) -> None:
        match state['game']['stage']:
            case GameStages.FIRST_STARTING_IS_AWAITED.value:
                print(MESSAGES['welcome'])
                self._request_first_game_starting()
            case GameStages.STARTING_IS_AWAITED.value:
                self._request_game_starting()
            case GameStages.DEPOSIT_IS_AWAITED.value:
                self._request_deposit()
            case GameStages.BET_IS_AWAITED.value:
                self._print_bet_request_preview(
                    state['statistics']['player']['money'])
                self._request_bet(
                    state['statistics']['player']['money'])
            case GameStages.CARD_TAKING_IS_AWAITED.value:
                self._print_card_taking_request_preview(state)
                self._request_card_taking()
            case GameStages.FINISHED.value:
                self._print_game_result(state)
                self._request_game_restart()
            case _:
                pass

    def _request_first_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input(MESSAGES['try_luck'])):
            self.emit(EventNames.GAME_STARTED)

    def _request_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input(MESSAGES['one_more_game'])):
            self.emit(EventNames.GAME_STARTED)

    def _request_deposit(self) -> None:
        while True:
            deposit = input(MESSAGES['deposit'])

            if deposit.isdigit():
                break

        self.emit(EventNames.MONEY_DEPOSITED, int(deposit))

    def _request_bet(self, player_money: int) -> None:
        while True:
            bet = input(
                f'Твоя ставка(мин. {MIN_BET}{RUBLE_SIGN}, макс. {player_money}{RUBLE_SIGN}): ')

            if bet.isdigit():
                bet_as_int = int(bet)

                if MIN_BET <= bet_as_int <= player_money:
                    break

        self.emit(EventNames.BET_MADE, bet_as_int)

    def _request_card_taking(self) -> None:
        if self._check_if_player_answer_affirmative(input(MESSAGES['one_more_card'])):
            self.emit(EventNames.CARD_TAKEN)
        else:
            self.emit(EventNames.CARD_REJECTED)

    def _request_game_restart(self) -> None:
        if self._check_if_player_answer_affirmative(input(MESSAGES['one_more_time'])):
            self.emit(EventNames.GAME_RESTARTED)

    def _check_if_player_answer_affirmative(self, answer: str) -> bool:
        return answer in AFFIRMATIVE_PLAYER_ANSWERS

    def _print_bet_request_preview(self, player_money: int) -> None:
        print(f'''
===================
Твои деньги: {player_money}{RUBLE_SIGN}
===================
''')

    def _print_card_taking_request_preview(self, state: State) -> None:
        print(f'''
===================
Банк: {state['game']['bank']}{RUBLE_SIGN}
-------------------
Твои деньги: {state['statistics']['player']['money']}{RUBLE_SIGN}
Твои карты: {state['game']['player']['deck']}
Твои очки: {state['game']['player']['score']}
===================
''')

    def _print_game_result(self, state: State) -> None:
        winner = state['game']['winner']

        print(f'''
===================
Победитель: {WINNER_TO_DISPLAYED_WINNER[winner or 'draw']}
-------------------
Твой результат:
  Карты: {state['game']['player']['deck']}
  Очки: {state['game']['player']['score']}
  Деньги: {state['statistics']['player']['money']}{RUBLE_SIGN}
  Выигрышей за все время: {state['statistics']['player']['wins']}
-------------------
Результат Skynet:
  Карты: {state['game']['computer']['deck']}
  Очки: {state['game']['computer']['score']}
  Выигрышей за все время: {state['statistics']['computer']['wins']}
===================
''')
