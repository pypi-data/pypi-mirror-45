import click

from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import DuplicationException
from edback.managers.key import KeyManager
from edback.utils import echo, style


@click.command('create')
@click.argument('name', metavar='<name>', type=click.STRING)
@pass_key_manager
def cli(key_manager: KeyManager, name):
    try:
        key_manager.create(name)
        echo.echo("Created key ", style.color(name, 'green'))
    except DuplicationException:
        echo.echo("The key name ", style.color(f"'{name}'", 'red'), " is duplicated")
