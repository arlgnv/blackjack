from savings import savings
from layers.view import view
from layers.presenter import presenter
from layers.model import model


class BlackJack:
    def __init__(self) -> None:
        self._view = view.View()
        self._model = model.Model()
        self._savings = savings.Savings(self._model)
        self._presenter = presenter.Presenter(self._view, self._model)
        self._model.init_state(
            self._savings.load_current_game(), self._savings.load_statistics())


BlackJack()
