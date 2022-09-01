from saver import Saver
from layers.view.view import View
from layers.presenter.presenter import Presenter
from layers.model import Game, EventNames as ModelEventNames
from layers.model.model import Model


class BlackJack:
    def __init__(self) -> None:
        self._saver = Saver()
        self._view = View()

        self._model = Model(self._saver.load_game())
        self._subscribe_to_model_events()

        self._presenter = Presenter(self._view, self._model)

        self._view.update(self._model.get_game_state())

    def _subscribe_to_model_events(self) -> None:
        self._model.on(ModelEventNames.GAME_FINISHED, self._handle_game_finish)

    def _handle_game_finish(self, game: Game) -> None:
        self._saver.save_game(game)


BlackJack()
