from typing import AnyStr

import click

from edback.commands.cmd_backups import pass_backup_manager
from edback.managers.backup import BackupManager
from edback.utils import echo, style


@click.command('remove')
@click.argument('hash', metavar='<hash>')
@pass_backup_manager
def cli(backup_manager: BackupManager, hash: AnyStr):
    backup = backup_manager.get(hash)
    if backup is None:
        echo.echo(style.color("Can't specify one backup", 'red'))
        return

    echo.echo("The backup '", style.color(str(backup), 'yellow'), "' will be removed")
    echo.echo("Do you really want to remove the backup '", style.color(str(backup), "yellow"), "'? [y/n]: ")
    answer = click.getchar()

    if answer == 'y':
        backup_manager.remove(backup.hash)
        echo.echo("The backup '", style.color(str(backup), 'yellow'), "' is removed")
    elif answer == 'n':
        echo.echo(style.color("Canceled", 'bright_yellow'))
    else:
        echo.echo(style.color("Wrong Input", 'red'))
