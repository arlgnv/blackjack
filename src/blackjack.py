from layers.view import view
from layers.presenter import presenter
from layers.model import model


class BlackJack:
    def __init__(self) -> None:
        self._view = view.View()
        self._model = model.Model()
        self._presenter = presenter.Presenter(self._view, self._model)

        self._view.update(self._model.get_state())


BlackJack()
