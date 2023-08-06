from typing import List, AnyStr, Union

import click


def echo(*messages: Union[List[AnyStr], AnyStr], **kwargs):
    kwargs.setdefault('nl', True)

    for message in messages:
        click.echo(message, nl=False)

    if kwargs['nl'] is True:
        click.echo()
