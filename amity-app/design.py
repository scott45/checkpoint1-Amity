__author__ = 'scotty'

import click
import sys
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format


def app_intro():
    click.secho('!' * 40, fg='yellow')
    click.secho('-' * 40, fg='white')
    init(strip=not sys.stdout.isatty())  # # strip colors if stdout is redirected
    cprint(figlet_format('Amity room allocation', font='big'), 'red')
    click.secho('-' * 40, fg='white')
    click.secho('!' * 40, fg='yellow')


def intro_msg():
    click.secho(
        """
    """""""""""'Add people, rooms and have them automatically allocated'"""""""""
        """, bold=True, fg='yellow')


def intro_header():
    click.clear()
    app_intro()

    with click.progressbar(range(10000), fill_char=click.style('(', fg='white', bg='red')) as prog_bar:
        for i in prog_bar:
            pass

    click.secho('' * 75)
    click.secho('' * 75)
    intro_msg()
