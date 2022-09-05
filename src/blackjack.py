from savings import Savings
from layers.view.view import View
from layers.presenter.presenter import Presenter
from layers.model import GameStages
from layers.model.model import Model


class BlackJack:
    def __init__(self) -> None:
        self._view = View()
        self._model = Model()
        self._savings = Savings(self._model)
        self._presenter = Presenter(self._view, self._model)

        game = self._savings.load_game()
        if game:
            self._model.update_game(game)

        statistics = self._savings.load_statistics()
        if statistics:
            self._model.update_statistics(statistics)

            if not game:
                self._model.update_game(
                    {'stage': GameStages.STARTING_IS_AWAITED})

        self._view.update(self._model.get_state())


BlackJack()
