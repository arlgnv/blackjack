from savings import Savings
from layers.view.view import View
from layers.presenter.presenter import Presenter
from layers.model.model import Model


class BlackJack:
    def __init__(self) -> None:
        self._view = View()
        self._model = Model()
        self._savings = Savings(self._model)
        self._presenter = Presenter(self._view, self._model)
        self._model.init_state(
            self._savings.load_current_game(), self._savings.load_statistics())


BlackJack()
