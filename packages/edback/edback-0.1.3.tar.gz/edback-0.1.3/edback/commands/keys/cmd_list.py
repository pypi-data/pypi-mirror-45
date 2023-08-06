import click

from edback.commands.cmd_keys import pass_key_manager
from edback.managers.key import KeyManager
from edback.utils import echo


@click.command('list')
@pass_key_manager
def cli(key_manager: KeyManager):
    echo.echo("Keys you having\n")
    keynames = key_manager.keys.keys()
    for keyname in keynames:
        echo.echo('  ' + keyname)
