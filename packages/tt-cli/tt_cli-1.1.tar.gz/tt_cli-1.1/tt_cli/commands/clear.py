from tt_cli.commands.abc import ABCCommand
from tt_cli import constants


class Command(ABCCommand):
    def handle(self):
        open(constants.FPATH, 'w').close()
