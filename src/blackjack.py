from savings import savings
from layers.view import view
from layers.presenter import presenter
from layers.model import model
import layers.model.types as model_types


class BlackJack:
    def __init__(self) -> None:
        self._view = view.View()
        self._model = model.Model()
        self._savings = savings.Savings(self._model)
        self._presenter = presenter.Presenter(self._view, self._model)

        self._start()

    def _start(self) -> None:
        state = self._model.get_state()

        current_game = self._savings.load_current_game()
        if current_game:
            state['game'] = current_game

        statistics = self._savings.load_statistics()
        if statistics:
            state['statistics'] = statistics

            if not current_game:
                state['game']['stage'] = model_types.GameStages.STARTING_IS_AWAITED.value

        self._model.set_state(state)


BlackJack()
