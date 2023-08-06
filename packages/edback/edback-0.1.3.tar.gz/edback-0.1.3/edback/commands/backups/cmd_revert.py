from typing import AnyStr

import click

from edback.commands.cmd_backups import pass_backup_manager
from edback.commands.cmd_keys import pass_key_manager
from edback.exceptions import CorruptedException
from edback.managers.backup import BackupManager
from edback.managers.key import KeyManager
from edback.utils import echo, style


@click.command('revert')
@click.argument('hash', metavar='<hash>', type=click.STRING)
@click.argument('keyname', metavar='<key>', type=click.STRING)
@click.argument('dest', default='.', metavar='<dest>', type=click.Path(resolve_path=True))
@pass_backup_manager
@pass_key_manager
def cli(key_manager: KeyManager, backup_manager: BackupManager, hash: AnyStr, keyname: AnyStr, dest: AnyStr):
    key = key_manager.get(keyname)
    if key is None:
        echo.echo(style.color("There isn't such key", 'red'))
        echo.echo("you can see keys using 'edback keys list'")
        return

    backup = backup_manager.get(hash)
    if backup is None:
        echo.echo(style.color("Can't specify one backup", 'red'))
        return

    try:
        backup_manager.revert(backup.hash, dest, key)
    except CorruptedException:
        echo.echo(style.color('An error occurred because the key and the backup file did not match.', 'red'))
