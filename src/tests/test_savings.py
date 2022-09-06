import os

from savings import savings as savings_module, constants as savings_constants


def test_load():
    savings = savings_module.Savings()

    if os.path.exists(savings_constants.SAVING_FILE_PATH):
        assert savings.load() is not None
    else:
        assert savings.load() is None
