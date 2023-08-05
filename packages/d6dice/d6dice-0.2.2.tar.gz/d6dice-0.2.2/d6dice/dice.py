
import numpy as np
from typing import Pattern, Any, List
import re

dice_pattern = re.compile(r'^(?P<count>\d+)[d/D](?P<sides>\d+)$')


def base_roller(count: int, sides: int) -> List[int]:
    _roles = []
    for role in range(count):
        _roles.extend(np.random.randint(1, sides+1, 1))
    return _roles


class D6Dice(object):
    """

    Attributes
    ----------
    dice: str with Pattern[ count d sides ] 

    """
    count: int
    sides: int
    _dice_pattern = dice_pattern
    _roller: Any
    _rolls: List 

    def __init__(self, dice: str = '1d6'):
        self.dice = self._dice_pattern.match(dice)

        self.count: int = int(self.dice.group('count'))

        self.sides: int = int(self.dice.group('sides'))

        self._roller = base_roller
        self._rolls = []

    def __repr__(self):
        return f'{self.__class__.__name__}(count={self.count}, sides={self.sides})'

    def __str__(self):
        return f'{self.count}d{self.sides}'

    def roll(self):
        rolls = [f'{self.__str__()}']
        rolls.extend(self._roller(self.count, self.sides))
        self._rolls.append(rolls)
        return rolls[1:]

    def set_roller(self, roller):
        setattr(self, '_roller', roller)

    #def _roller(self, sides: int):
    #    return np.random.randint(1, sides+1, 1)[0]

    @property
    def rolls(self):
        return self._rolls

    @property
    def max(self):
        return self.count * self.sides

