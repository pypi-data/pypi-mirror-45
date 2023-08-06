from typing import AnyStr

import click

from edback.commands.cmd_backups import pass_backup_manager
from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import DuplicationException
from edback.managers.backup import BackupManager
from edback.managers.key import KeyManager
from edback.utils import echo, style


@click.command('create')
@click.argument('message', metavar='<message>', type=click.STRING)
@click.argument('keyname', metavar='<key>', type=click.STRING)
@click.argument('path', default='.', metavar='<path>', type=click.Path(resolve_path=True))
@click.option('-t', '--tags', default='', type=click.STRING)
@pass_backup_manager
@pass_key_manager
def cli(key_manager: KeyManager, backup_manager: BackupManager, message: AnyStr, keyname: AnyStr, path: AnyStr, tags):
    tags = tags.split(',')
    tags = list(filter(lambda x: x != '', tags))

    key = key_manager.get(keyname)
    if key is None:
        echo.echo("There isn't the key named '", style.color(keyname, "red"), "'")
        return

    try:
        backup = backup_manager.create(message, path, tags, key)
    except DuplicationException as e:
        duplicated_hash = e.duplicated_object
        backup = backup_manager.get(duplicated_hash)

        echo.echo(
            style.color(f"Looks like there's the same backups! ", 'bright_green'),
            style.color(f"{str(backup)}", 'yellow'))
        return

    echo.echo(f"[{backup.hash}] {message}")
    echo.echo("from '", style.color(backup.path, 'magenta'))
    echo.echo("tags: [", style.color(" ".join(backup.tags), 'bright_yellow'), "]")
