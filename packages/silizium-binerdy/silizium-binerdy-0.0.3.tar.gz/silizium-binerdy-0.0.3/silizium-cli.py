#!/usr/bin/env python3
import click
from silizium.use_cases.silizium_use_cases import philosophy_game


@click.command()
@click.option(
    '-w', '--word', type=click.STRING, required=True,
    help='use word as starting point to test wikipedia philosophy game.'
)
@click.option(
    '-l', '--limit', type=click.INT, default=5,
    help='limit number of url calls. (default is 5)'
)
@click.option(
    '--headless', '--gui', default=True,
    help='run engine with headless option'
)
def silizium(word, limit, headless):
    click.echo(f'starting silizium mode in headless={headless}')
    click.echo(f'start word={word}')
    click.echo(f'limit url calls to {limit}\n')

    for valid_link in philosophy_game(word, limit, headless):
        click.echo(valid_link)


if __name__ == '__main__':
    silizium()
