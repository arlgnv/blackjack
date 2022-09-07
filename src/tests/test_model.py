import unittest
import os

from layers.model import model, constants as model_constants, types as model_types
from savings import savings, constants as savings_constants


class TestModel(unittest.TestCase):
    def test_init(self):
        model_instance = model.Model(savings.Savings())
        state = model_instance.get_state()

        if os.path.exists(savings_constants.SAVING_FILE_PATH):
            self.assertNotEqual(state, model_constants.INITIAL_STATE)
        else:
            self.assertEqual(state, model_constants.INITIAL_STATE)

    def test_start_game(self):
        model_instance = model.Model(savings.Savings())

        model_instance.start_game()
        self.assertEqual(model_instance.get_state()[
                         'game']['stage'], model_types.GameStages.BET_IS_AWAITED.value)

    def test_add_money_to_player(self):
        model_instance = model.Model(savings.Savings())

        if os.path.exists(savings_constants.SAVING_FILE_PATH):
            saved_money = model_instance.get_state(
            )['statistics']['player']['money']

            model_instance.add_money_to_player(10)
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], saved_money + 10)
        else:
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], model_constants.INITIAL_STATE['statistics']['player']['money'])
            model_instance.add_money_to_player(10)
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], model_constants.INITIAL_STATE['statistics']['player']['money'] + 10)

    def test_make_bet_for_player(self):
        model_instance = model.Model(savings.Savings())

        if os.path.exists(savings_constants.SAVING_FILE_PATH):
            saved_money = model_instance.get_state(
            )['statistics']['player']['money']

            model_instance.make_bet_for_player(10)
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], saved_money - 10)
        else:
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], model_constants.INITIAL_STATE['statistics']['player']['money'])
            model_instance.make_bet_for_player(10)
            self.assertEqual(model_instance.get_state(
            )['statistics']['player']['money'], model_constants.INITIAL_STATE['statistics']['player']['money'] - 10)

    def test_issue_card_to_player(self):
        model_instance = model.Model(savings.Savings())

        if os.path.exists(savings_constants.SAVING_FILE_PATH):
            saved_deck_size = len(model_instance.get_state()
                                  ['game']['player']['deck'])

            model_instance.issue_card_to_player()
            self.assertEqual(len(model_instance.get_state()[
                'game']['player']['deck']), saved_deck_size + 1)
        else:
            self.assertEqual(len(model_instance.get_state()[
                'game']['player']['deck']), 0)
            model_instance.issue_card_to_player()
            self.assertEqual(len(model_instance.get_state()[
                'game']['player']['deck']), 1)

    def test_finish_game(self):
        model_instance = model.Model(savings.Savings())

        model_instance.finish_game()
        self.assertEqual(model_instance.get_state()[
            'game']['stage'], model_types.GameStages.FINISHED.value)


if __name__ == '__main__':
    unittest.main()
