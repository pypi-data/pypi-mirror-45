import datetime
from tt import constants


def getnow() -> str:
    return datetime.datetime.now().strftime(constants.DTFORMAT)
