from observable.observable import Observable
from layers.model.types import State

from layers.view.utils import check_if_user_response_affirmative


class View(Observable):
    def __init__(self):
        super().__init__()

        with open('src/messages/welcome.txt', 'r', encoding='utf-8') as welcome_message:
            print(welcome_message.read())

    def display_status(self, state: State):
        print(f'''
Банк: {state['bank']}
Твои карты: {state['player']['deck']}
Твои очки: {state['player']['score']}
''')

    def request_bet(self, state: State):
        bet = int(input(f'Твоя ставка(макс. {state["player"]["money"]}): '))

        self.notify('betMade', bet)

    def request_card_taking(self):
        if check_if_user_response_affirmative(input('Возьмем еще карту? [y/n] ').lower()):
            self.notify('cardTaken')
