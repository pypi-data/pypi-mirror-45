import json
from typing import AnyStr, TextIO

import click

from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import DuplicationException, NotExistsException
from edback.managers.key import KeyManager
from edback.structures.key import Key
from edback.utils import echo, style


@click.command('import')
@click.argument('name', metavar='<name>', type=click.STRING)
@click.argument('keyfile', metavar='<keyfile>', type=click.File('w'))
@pass_key_manager
def cli(key_manager: KeyManager, name: AnyStr, keyfile: TextIO):
    key = key_manager.get(name)
    if key is None:
        echo.echo("There isn't the key named '", style.color(name, "red"), "'")

    json.dump(key.serialize(), keyfile)
    echo.echo("Exported a key named '", style.color(name, 'yellow'))

