from typing import AnyStr, TextIO

import click

from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import DuplicationException, CorruptedException
from edback.managers.key import KeyManager
from edback.structures.key import Key
from edback.utils import echo, style


@click.command('import')
@click.argument('name', metavar='<name>', type=click.STRING)
@click.argument('keyfile', metavar='<keyfile>', type=click.File('r'))
@pass_key_manager
def cli(key_manager: KeyManager, name: AnyStr, keyfile: TextIO):
    key = Key.from_file(keyfile)

    try:
        key_manager.add(name, key)
        echo.echo("Imported key ", style.color(name, 'green'))
    except DuplicationException:
        echo.echo("The key name ", style.color(f"'{name}'", 'red'), " is duplicated")
    except CorruptedException:
        echo.echo(style.color("The keyfile looks like corrupted", "red"))

