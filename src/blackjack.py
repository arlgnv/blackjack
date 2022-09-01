from saver import Saver
from layers.presenter import EventNames
from layers.presenter.presenter import Presenter
from layers.model import Game


class BlackJack:
    def __init__(self) -> None:
        self._saver = Saver()

        self._presenter = Presenter()
        self._subscribe_to_presenter_events()

    def start(self) -> None:
        self._presenter.start()

    def _subscribe_to_presenter_events(self) -> None:
        self._presenter.on(EventNames.GAME_FINISHED, self._handle_game_finish)

    def _handle_game_finish(self, game: Game) -> None:
        self._saver.save_game(game)


black_jack = BlackJack()
black_jack.start()
