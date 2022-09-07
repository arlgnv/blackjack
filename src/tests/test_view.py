import unittest
from mock import patch
import copy
from typing import Any

from layers.view import view as view_layer, constants as view_constants
from layers.model import constants as model_constants, types as model_types

view = view_layer.View()


class TestView(unittest.TestCase):
    @patch('builtins.print')
    @patch('builtins.input', lambda _: '')
    def test_update_when_game_starting(self, mock_print: Any):
        view.update(model_constants.INITIAL_STATE)
        mock_print.assert_called_with(view_constants.MESSAGES['welcome'])

    @patch('builtins.print')
    @patch('builtins.input', lambda _: '0')
    def test_update_when_deposit_is_awaited(self, mock_print: Any):
        state = copy.deepcopy(model_constants.INITIAL_STATE)
        state['game']['stage'] = model_types.GameStages.DEPOSIT_IS_AWAITED.value
        view.update(state)
        mock_print.assert_not_called()

    @patch('builtins.print')
    @patch('builtins.input', lambda _: '0')
    def test_update_when_bet_is_awaited(self, mock_print: Any):
        state = copy.deepcopy(model_constants.INITIAL_STATE)
        state['game']['stage'] = model_types.GameStages.FINISHED.value
        view.update(state)
        mock_print.assert_called()

    @patch('builtins.print')
    @patch('builtins.input', lambda _: '')
    def test_update_when_card_taking_is_awaited(self, mock_print: Any):
        state = copy.deepcopy(model_constants.INITIAL_STATE)
        state['game']['stage'] = model_types.GameStages.CARD_TAKING_IS_AWAITED.value
        view.update(state)
        mock_print.assert_called()

    @patch('builtins.print')
    @patch('builtins.input', lambda _: '')
    def test_update_when_game_finished(self, mock_print: Any):
        state = copy.deepcopy(model_constants.INITIAL_STATE)
        state['game']['stage'] = model_types.GameStages.FINISHED.value
        view.update(state)
        mock_print.assert_called()
