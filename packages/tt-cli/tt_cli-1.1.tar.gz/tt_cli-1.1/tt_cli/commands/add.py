import csv

from tt_cli.commands.abc import ABCCommand
from tt_cli import constants
from tt_cli import utils


class Command(ABCCommand):
    def add_arguments(self, parser):
        parser.add_argument('amount', help='Amount, hours', type=int)
        parser.add_argument('comment', help='Comment', nargs='+')

    def handle(self, amount, comment):
        amount = int(amount)
        assert amount > 0
        assert comment
        comment = " ".join(comment)

        with open(constants.FPATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([
                utils.getnow(),
                amount,
                comment,
            ])
