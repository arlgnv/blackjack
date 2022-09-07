import unittest
import os

from savings import savings, constants as savings_constants
from layers.model import constants as model_constants


class TestSavings(unittest.TestCase):
    def test_load(self):
        savings_instance = savings.Savings()

        if os.path.exists(savings_constants.SAVING_FILE_PATH):
            self.assertIsNotNone(savings_instance.load())
        else:
            self.assertIsNone(savings_instance.load())

    def test_save(self):
        savings_instance = savings.Savings()

        if not os.path.exists(savings_constants.SAVING_FILE_PATH):
            savings_instance.save(model_constants.INITIAL_STATE)

            self.assertTrue(os.path.exists(savings_constants.SAVING_FILE_PATH))
