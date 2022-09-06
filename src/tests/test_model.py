import copy

from layers.model import model as model_layer, constants as model_constants, types as model_types


# def test_init():
#     model = model_layer.Model()
#     state = model.get_state()

#     assert state == model_constants.INITIAL_STATE


# def test_update():
#     model = model_layer.Model()

#     assert model.get_state()['game']['bank'] == 0

#     new_state = copy.deepcopy(model_constants.INITIAL_STATE)
#     new_state['game']['bank'] = 10
#     model.set_state(new_state)

#     assert model.get_state()['game']['bank'] == 10


def test_start_game():
    model = model_layer.Model()

    model.start_game()

    assert model.get_state()[
        'game']['stage'] == model_types.GameStages.BET_IS_AWAITED.value


def test_add_money_to_player():
    model = model_layer.Model()

    assert model.get_state()['statistics']['player']['money'] == 50
    model.add_money_to_player(10)
    assert model.get_state()['statistics']['player']['money'] == 60


def test_make_bet_for_player():
    model = model_layer.Model()

    assert model.get_state()['statistics']['player']['money'] == 50
    model.make_bet_for_player(10)
    assert model.get_state()['statistics']['player']['money'] == 40


def test_issue_card_to_player():
    model = model_layer.Model()

    assert len(model.get_state()['game']['player']['deck']) == 0
    model.issue_card_to_player()
    assert len(model.get_state()['game']['player']['deck']) == 1


def test_finish_game():
    model = model_layer.Model()

    model.finish_game()
    assert model.get_state()[
        'game']['stage'] == model_types.GameStages.FINISHED.value
