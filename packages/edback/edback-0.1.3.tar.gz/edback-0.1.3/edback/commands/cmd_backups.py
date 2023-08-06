import click

from edback.managers.backup import BackupManager
from edback.utils.cli import SimpleMultiCommand


class CLI(SimpleMultiCommand):
    commands_packages = "edback.commands.backups"


pass_backup_manager = click.make_pass_decorator(BackupManager, ensure=True)


@click.group(cls=CLI)
def cli():
    pass
