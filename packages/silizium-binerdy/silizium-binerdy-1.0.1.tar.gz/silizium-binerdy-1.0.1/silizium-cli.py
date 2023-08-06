#!/usr/bin/env python3
import os
import click
from silizium.use_cases.silizium_use_cases import philosophy_game
from silizium.domain.language import get_target_url
from silizium.domain.csv_parser import (
    words_as_list,
    update_words,
    words_to_csv
)


@click.group()
def silizium():
    pass

@silizium.command('single')
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
def single(word, limit, headless):
    click.echo(f'starting silizium mode in headless={headless}')
    click.echo(f'start word={word}')
    click.echo(f'limit url calls to {limit}\n')

    for valid_link, links_visited in philosophy_game(word, limit, headless):
        click.echo(valid_link)
    test_result = valid_link == get_target_url('de')
    words = words_as_list()
    words = update_words(words, word, test_result, links_visited)
    if links_visited != limit:
        words = update_words(words, word, False, limit)
    words_to_csv(sorted(words))
    click.echo('\n')

@silizium.command('multi')
def multi():
    words = words_as_list()
    for p in words:
        word = p[0]
        limit = 30 if p[2] is None else p[2]
        os.system(f'silizium-cli.py single -w "{word}" -l "{limit}"')


if __name__ == '__main__':
    silizium()
