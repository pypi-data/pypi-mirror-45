import os

DTFORMAT = os.getenv("TT_DTFORMAT", "%Y-%m-%d %H:%M:%S")
FPATH = os.getenv("TT_FPATH", os.path.expanduser('~/.tt.csv'))
TABLEROW = "%-35s | %5s hrs | %s"
TABLE_DELIMITER = "-" * (55)
