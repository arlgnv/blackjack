from layers.view import view as view_layer, constants as view_constants
from layers.model import constants as model_constants


def test_update(capsys, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    view = view_layer.View()
    view.update(model_constants.INITIAL_STATE)

    captured = capsys.readouterr()

    assert captured.out.strip() == view_constants.MESSAGES['welcome'].strip()
