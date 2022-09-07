from savings import savings
from layers.view import view
from layers.presenter import presenter
from layers.model import model


class BlackJack:
    _savings: savings.Savings
    _view: view.View
    _model: model.Model
    _presenter: presenter.Presenter

    def __init__(self) -> None:
        self._savings = savings.Savings()
        self._view = view.View()
        self._model = model.Model(self._savings)
        self._presenter = presenter.Presenter(self._view, self._model)

        self._view.update(self._model.get_state())


BlackJack()
