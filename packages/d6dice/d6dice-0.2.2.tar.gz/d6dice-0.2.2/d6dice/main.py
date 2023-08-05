from .dice import D6Dice


def cli():
    die = D6Dice('2d6')

    print(f'Dice: {die}')
    print(f'Die count: {die.count}')
    print(f'Die sides: {die.sides}')
    print(f'Dice max roll: {die.max}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice rolls: {die._rolls}')


    die = D6Dice('4D6')

    print(f'Dice: {die}')
    print(f'Die count: {die.count}')
    print(f'Die sides: {die.sides}')
    print(f'Dice max roll: {die.max}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice rolls: {die._rolls}')

    die = D6Dice('12d8')

    print(f'Dice: {die}')
    print(f'Die count: {die.count}')
    print(f'Die sides: {die.sides}')
    print(f'Dice max roll: {die.max}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice rolls: {die._rolls}')

    die = D6Dice('1d48')

    print(f'Dice: {die}')
    print(f'Die count: {die.count}')
    print(f'Die sides: {die.sides}')
    print(f'Dice max roll: {die.max}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice roll: {die.roll()}')
    print(f'Dice rolls: {die._rolls}')
