import argparse
from tt.commands import COMMANDS


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    for cmd_name, handler in COMMANDS.items():
        handler.add_arguments(subparsers.add_parser(cmd_name))

    kwargs = vars(parser.parse_args())
    command = kwargs.pop('subparser')

    COMMANDS[command].handle(**kwargs)
