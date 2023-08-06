import csv
import datetime

from tt.commands.abc import ABCCommand
from tt import constants


class Command(ABCCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            'days', help='Days to show', type=int, default=45, nargs="?")

    def handle(self, days=45):
        now = datetime.datetime.now()

        with open(constants.FPATH, 'r+') as f:
            reader = csv.reader(f)
            print(constants.TABLEROW % ("DATE", "SPENT", "TASK"))
            print(constants.TABLE_DELIMITER)

            hrsum = 0
            for line in reader:
                dtstr, hours, task = line

                dt = datetime.datetime.strptime(dtstr, constants.DTFORMAT)
                delta = now - dt

                if delta.days <= days:
                    hours = int(hours)
                    hrsum += hours
                    print(constants.TABLEROW % (
                        f"{dt} ({delta.days} days ago)",
                        hours,
                        task)
                    )

            print(constants.TABLE_DELIMITER)
            print(f"Total %s hours" % hrsum)
