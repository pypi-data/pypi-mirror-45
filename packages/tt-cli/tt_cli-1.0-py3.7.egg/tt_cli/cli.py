import argparse
from tt_cli.commands import COMMANDS


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    for cmd_name, handler in COMMANDS.items():
        handler.add_arguments(subparsers.add_parser(cmd_name))

    kwargs = vars(parser.parse_args())
    command = kwargs.pop('subparser')

    if command not in COMMANDS:
        parser.print_usage()
    else:
        COMMANDS[command].handle(**kwargs)
