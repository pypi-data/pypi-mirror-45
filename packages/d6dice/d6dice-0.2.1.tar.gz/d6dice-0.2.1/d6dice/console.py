
from .dice import D6Dice
import cmd
import click

class D6Console(cmd.Cmd):
    intro = 'Dice console'
    prompt = '<dice> '
    dice: D6Dice

    def preloop(self):
        self.dice = D6Dice()

    def postloop(self):
        print(f'Dice rolls: {self.dice.rolls}')

    def do_set(self, dice: str):
        self.dice = D6Dice(dice)

    def do_show(self, arg):
        print(f'Dice: {self.dice}\nDice rolls: {self.dice.rolls}')

    def do_roll(self, dice: str):
        if dice:
            self.dice = D6Dice(dice)

        print(f'{self.dice.roll()}')

    def do_exit(self, arg):
        return True

    def emptyline(self):
        pass


@click.group('dice')
def cli():
    pass

@cli.command('run')
@click.argument('command', nargs=-1, type=click.STRING)
def run_cmd(command):
    cmd = ' '.join(command)
    CliApp = D6Console()
    click.secho(f'command: {cmd}')
    CliApp.preloop()
    CliApp.onecmd(cmd)

@cli.command('shell')
def run_shell():
    CliApp = D6Console()
    CliApp.cmdloop()
