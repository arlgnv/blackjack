from observable import observable
import layers.model.constants as ModelConstants
import layers.model.types as ModelTypes

from . import constants, types


class View(observable.Observable):
    def update(self, state: ModelTypes.State) -> None:
        match state['game']['stage']:
            case ModelTypes.GameStages.FIRST_STARTING_IS_AWAITED.value:
                print(constants.MESSAGES['welcome'])
                self._request_first_game_starting()
            case ModelTypes.GameStages.STARTING_IS_AWAITED.value:
                self._request_game_starting()
            case ModelTypes.GameStages.DEPOSIT_IS_AWAITED.value:
                self._request_deposit()
            case ModelTypes.GameStages.BET_IS_AWAITED.value:
                self._print_bet_request_preview(
                    state['statistics']['player']['money'])
                self._request_bet(
                    state['statistics']['player']['money'])
            case ModelTypes.GameStages.CARD_TAKING_IS_AWAITED.value:
                self._print_card_taking_request_preview(state)
                self._request_card_taking()
            case ModelTypes.GameStages.FINISHED.value:
                self._print_game_result(state)
                self._request_game_restart()
            case _:
                pass

    def _request_first_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input(constants.MESSAGES['try_luck'])):
            self.emit(types.EventNames.GAME_STARTED)

    def _request_game_starting(self) -> None:
        if self._check_if_player_answer_affirmative(input(constants.MESSAGES['one_more_game'])):
            self.emit(types.EventNames.GAME_STARTED)

    def _request_deposit(self) -> None:
        while True:
            deposit = input(constants.MESSAGES['deposit'])

            if deposit.isdigit():
                break

        self.emit(types.EventNames.MONEY_DEPOSITED, int(deposit))

    def _request_bet(self, player_money: int) -> None:
        while True:
            bet = input(
                f'Твоя ставка(мин. {ModelConstants.MIN_BET}{constants.RUBLE_SIGN}, макс. {player_money}{constants.RUBLE_SIGN}): ')

            if bet.isdigit():
                bet_as_int = int(bet)

                if ModelConstants.MIN_BET <= bet_as_int <= player_money:
                    break

        self.emit(types.EventNames.BET_MADE, bet_as_int)

    def _request_card_taking(self) -> None:
        if self._check_if_player_answer_affirmative(input(constants.MESSAGES['one_more_card'])):
            self.emit(types.EventNames.CARD_TAKEN)
        else:
            self.emit(types.EventNames.CARD_REJECTED)

    def _request_game_restart(self) -> None:
        if self._check_if_player_answer_affirmative(input(constants.MESSAGES['one_more_time'])):
            self.emit(types.EventNames.GAME_RESTARTED)

    def _check_if_player_answer_affirmative(self, answer: str) -> bool:
        return answer in constants.AFFIRMATIVE_PLAYER_ANSWERS

    def _print_bet_request_preview(self, player_money: int) -> None:
        print(f'''
===================
Твои деньги: {player_money}{constants.RUBLE_SIGN}
===================
''')

    def _print_card_taking_request_preview(self, state: ModelTypes.State) -> None:
        print(f'''
===================
Банк: {state['game']['bank']}{constants.RUBLE_SIGN}
-------------------
Твои деньги: {state['statistics']['player']['money']}{constants.RUBLE_SIGN}
Твои карты: {state['game']['player']['deck']}
Твои очки: {state['game']['player']['score']}
===================
''')

    def _print_game_result(self, state: ModelTypes.State) -> None:
        winner = state['game']['winner']

        print(f'''
===================
Победитель: {constants.WINNER_TO_DISPLAYED_WINNER[winner or 'draw']}
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
