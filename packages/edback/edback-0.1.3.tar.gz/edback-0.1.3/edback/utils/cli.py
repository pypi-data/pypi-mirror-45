import os
import sys
import click

from typing import List, AnyStr, Union
from types import ModuleType


class SimpleMultiCommand(click.MultiCommand):
    commands_packages = ""

    def list_commands(self, ctx: click.Context) -> List[AnyStr]:
        commands_folder = self.commands_packages.replace('.', '/')
        root_path = os.path.dirname(__file__)
        commands_folder = os.path.abspath(os.path.join(root_path, '..', '..', commands_folder))

        commands = list()
        for filename in os.listdir(commands_folder):
            if filename.startswith('cmd_') and filename.endswith('.py'):
                commands.append(filename[4:-3])
        return commands

    def get_command(self, ctx: click.Context, name: AnyStr) -> Union[None, ModuleType]:
        try:
            module = __import__(f'{self.commands_packages}.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return module.cli
