from tt_cli.commands import (
    add,
    days,
    show,
    clear,
)


COMMANDS = {
    'add': add.Command(),
    'days': days.Command(),
    'show': show.Command(),
    'clear': clear.Command(),
}
