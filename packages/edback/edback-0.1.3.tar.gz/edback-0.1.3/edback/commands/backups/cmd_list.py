import re
from datetime import datetime
from typing import List, AnyStr, Tuple

import click

from edback.commands.cmd_backups import pass_backup_manager
from edback.managers.backup import BackupManager
from edback.structures.backup import Backup
from edback.utils import style, echo

BACKUP_OUTPUT_FORMAT = """backup {hash} [{tags}]
Date: {created_at}

    {message}

"""


def _generate_backups_output(backups: List[Backup]):
    for backup in backups:
        created_at = datetime.fromtimestamp(backup.created_at).strftime("%Y %m %d, %H:%M:%S")
        tags = ''.join(backup.tags)

        output = BACKUP_OUTPUT_FORMAT.format(
            hash=backup.hash,
            message=backup.message,
            created_at=created_at,
            tags=tags,
        )

        lines = output.split('\n')

        lines[0] = style.color(lines[0], 'yellow')

        yield '\n'.join(lines)


@click.command('list')
@click.option('-df', '--date-from', default='1999-01-01', type=click.DateTime())
@click.option('-dt', '--date-to', default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type=click.DateTime())
@click.option('-t', '--tag', multiple=True, type=click.STRING)
@click.option('-r', '--regex', default='.*', type=click.STRING)
@pass_backup_manager
def cli(backup_manager: BackupManager, date_from: datetime, date_to: datetime, tag: Tuple[AnyStr], regex: AnyStr):
    backups: List[Backup] = backup_manager.backups.values()
    tags = set(tag)

    def check_period(backup) -> bool:
        created_at = datetime.fromtimestamp(backup.created_at)
        return date_from < created_at < date_to

    def check_tags(backup) -> bool:
        return tags.issubset(backup.tags)

    def check_message_by_regex(backup) -> bool:
        return re.match(regex, backup.message) is not None

    backups = list(filter(check_tags, backups))  # by tags
    backups = list(filter(check_message_by_regex, backups))  # by regex
    backups = list(filter(check_period, backups))  # by date

    if len(backups) is 0:
        echo.echo(style.color("There aren't no backups by condition", 'bright_yellow'))
        return

    backups.sort(key=lambda backup: backup.created_at, reverse=True)  # by time created

    click.echo_via_pager(_generate_backups_output(backups))
