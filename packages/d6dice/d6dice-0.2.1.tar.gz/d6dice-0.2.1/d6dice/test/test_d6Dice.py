
from d6dice.dice import D6Dice
import pytest

TEST_DICE = ['1d6', '2d6', '4d6', '2d12', '6d18']

@pytest.fixture(scope='module', params=TEST_DICE)
def test_dice(request):
    return request.param


class TestD6Dice:

    def test_roll(self, test_dice):
        dice = D6Dice(test_dice)
        assert f'{dice.count}d{dice.sides}' == test_dice
        assert type(dice.roll()) is list

    def test_rolls(self, test_dice):
        dice = D6Dice(test_dice)
        dice.roll()
        dice.roll()
        dice.roll()
        assert len(dice.rolls) == 3


    # def test_max(self, ):
    #     self.fail()
