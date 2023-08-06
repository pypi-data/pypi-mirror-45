from tt.commands.abc import ABCCommand
from tt import constants


class Command(ABCCommand):
    def handle(self):
        open(constants.FPATH, 'w').close()
