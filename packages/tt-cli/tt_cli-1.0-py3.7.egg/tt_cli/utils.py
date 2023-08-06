import datetime
from tt_cli import constants


def getnow() -> str:
    return datetime.datetime.now().strftime(constants.DTFORMAT)
