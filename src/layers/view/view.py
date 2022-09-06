from observable import observable
from layers.model import constants as model_constants, types as model_types

from . import constants, types


class View(observable.Observable):
    def update(self, state: model_types.State) -> None:
        match state['game']['stage']:
            case model_types.GameStages.FIRST_STARTING_IS_AWAITED.value:
                print(constants.MESSAGES['welcome'])
                self._request_first_game_starting()
            case model_types.GameStages.STARTING_IS_AWAITED.value:
                self._request_game_starting()
            case model_types.GameStages.DEPOSIT_IS_AWAITED.value:
                self._request_deposit()
            case model_types.GameStages.BET_IS_AWAITED.value:
                self._print_bet_request_preview(
                    state['statistics']['player']['money'])
                self._request_bet(
                    state['statistics']['player']['money'])
            case model_types.GameStages.CARD_TAKING_IS_AWAITED.value:
                self._print_card_taking_request_preview(state)
                self._request_card_taking()
            case model_types.GameStages.FINISHED.value:
                self._print_game_result(state)
                self._request_game_restart()
            case _:
                pass

    def _request_first_game_starting(self) -> None:
        request_text = constants.REQUESTS['try_luck']

        if self._check_if_player_answer_affirmative(input(request_text)):
            self._emit(types.EventNames.GAME_STARTED.value)

    def _request_game_starting(self) -> None:
        request_text = constants.REQUESTS['one_more_game']

        if self._check_if_player_answer_affirmative(input(request_text)):
            self._emit(types.EventNames.GAME_STARTED.value)

    def _request_deposit(self) -> None:
        request_text = constants.REQUESTS['deposit']

        while True:
            deposit = input(request_text)

            if deposit.isdigit():
                break

        self._emit(types.EventNames.MONEY_DEPOSITED.value, int(deposit))

    def _request_bet(self, player_money: int) -> None:
        request_text = f'Твоя ставка(мин. {model_constants.MIN_BET}{constants.RUBLE_SIGN}, макс. {player_money}{constants.RUBLE_SIGN}): '

        while True:
            bet = input(request_text)

            if bet.isdigit():
                bet_as_int = int(bet)

                if model_constants.MIN_BET <= bet_as_int <= player_money:
                    break

        self._emit(types.EventNames.BET_MADE.value, bet_as_int)

    def _request_card_taking(self) -> None:
        request_text = constants.REQUESTS['one_more_card']

        if self._check_if_player_answer_affirmative(input(request_text)):
            self._emit(types.EventNames.CARD_TAKEN.value)
        else:
            self._emit(types.EventNames.CARD_REJECTED.value)

    def _request_game_restart(self) -> None:
        request_text = constants.REQUESTS['one_more_time']

        if self._check_if_player_answer_affirmative(input(request_text)):
            self._emit(types.EventNames.GAME_RESTARTED.value)

    def _check_if_player_answer_affirmative(self, answer: str) -> bool:
        return answer in constants.AFFIRMATIVE_PLAYER_ANSWERS

    def _print_bet_request_preview(self, player_money: int) -> None:
        print(f'''
===================
Твои деньги: {player_money}{constants.RUBLE_SIGN}
===================
''')

    def _print_card_taking_request_preview(self, state: model_types.State) -> None:
        print(f'''
===================
Банк: {state['game']['bank']}{constants.RUBLE_SIGN}
-------------------
Твои деньги: {state['statistics']['player']['money']}{constants.RUBLE_SIGN}
Твои карты: {state['game']['player']['deck']}
Твои очки: {state['game']['player']['score']}
===================
''')

    def _print_game_result(self, state: model_types.State) -> None:
        print(f'''
===================
Победитель: {constants.WINNER_TO_DISPLAYED_WINNER[state['game']['winner'] or 'draw']}
-------------------
Твой результат:
  Карты: {state['game']['player']['deck']}
  Очки: {state['game']['player']['score']}
  Деньги: {state['statistics']['player']['money']}{constants.RUBLE_SIGN}
  Выигрышей за все время: {state['statistics']['player']['wins']}
-------------------
Результат Skynet:
  Карты: {state['game']['computer']['deck']}
  Очки: {state['game']['computer']['score']}
  Выигрышей за все время: {state['statistics']['computer']['wins']}
===================
''')
