from observable.observable import Observable
from layers.model.types import State


class View(Observable):
    def __init__(self, state: State):
        super().__init__()

        with open('src/messages/welcome.txt', 'r', encoding='utf-8') as welcome_message:
            print(welcome_message.read())

        self._request_bet(state)

    def display_status(self, state: State):
        print(f'''
Твои карты: {state['player']['deck']}
Твои очки: {state['player']['score']}
''')

        if state['is_finished']:
            print('Игра окончена')
        else:
            self._request_card_taking()

    def _request_bet(self, state: State):
        bet = int(input(f'Твоя ставка(макс. {state["player"]["money"]}): '))

        self.notify('betMade', bet)

    def _request_card_taking(self):
        if self._check_if_player_response_affirmative(input('Возьмем еще карту? [y/n] ').lower()):
            self.notify('cardTaken')
        else:
            self.notify('gameFinished')

    def _check_if_player_response_affirmative(self, response: str):
        return response in ('', 'y')
