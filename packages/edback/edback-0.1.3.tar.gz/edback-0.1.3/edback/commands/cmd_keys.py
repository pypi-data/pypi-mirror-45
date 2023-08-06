import click

from edback.managers.key import KeyManager
from edback.utils.cli import SimpleMultiCommand


class CLI(SimpleMultiCommand):
    commands_packages = "edback.commands.keys"


pass_key_manager = click.make_pass_decorator(KeyManager, ensure=True)


@click.group(cls=CLI)
def cli():
    pass
