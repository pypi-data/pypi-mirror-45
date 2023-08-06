from typing import AnyStr

import click

from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import NotExistsException
from edback.managers.key import KeyManager
from edback.utils import echo, style


@click.command('remove')
@click.argument('name', metavar='<name>')
@pass_key_manager
def cli(key_manager: KeyManager, name: AnyStr):
    echo.echo("The key '", style.color(name, 'yellow'), "' will be removed")
    echo.echo("Do you really want to remove the key '", style.color(name, "yellow"), "'? [y/n]: ")
    answer = click.getchar()

    if answer == 'y':
        try:
            key_manager.remove(name)
            echo.echo("The key '", style.color(name, 'yellow'), "' is removed")
        except NotExistsException:
            echo.echo("There isn't the key named '", style.color(name, "red"), "'")
    elif answer == 'n':
        echo.echo(style.color("Canceled", 'bright_yellow'))
    else:
        echo.echo(style.color("Wrong Input", 'red'))
