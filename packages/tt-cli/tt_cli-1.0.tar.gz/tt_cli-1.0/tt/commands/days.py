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

        dayresult = {}

        with open(constants.FPATH, 'r+') as f:
            reader = csv.reader(f)

            hrsum = 0
            for line in reader:
                dtstr, hours, task = line
                hours = int(hours)
                dt = datetime.datetime.strptime(dtstr, constants.DTFORMAT)
                delta = now - dt

                if delta.days <= days:
                    hrsum += hours

                    dtdate = dt.date()
                    if dtdate not in dayresult:
                        dayresult[dtdate] = 0
                    dayresult[dtdate] += hours

        print(constants.TABLEROW % ("DATE", "SPENT", ""))
        print(constants.TABLE_DELIMITER)
        for date, hours in dayresult.items():
            print(constants.TABLEROW % (date, hours, ""))
        print(constants.TABLE_DELIMITER)
        print(f"Total %s hours" % hrsum)
