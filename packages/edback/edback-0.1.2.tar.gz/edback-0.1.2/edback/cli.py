import click

from edback.utils.cli import SimpleMultiCommand


class CLI(SimpleMultiCommand):
    commands_packages = "edback.commands"


@click.group(cls=CLI, help="CLI Application to support encryption, decryption for backup")
def cli():
    pass
