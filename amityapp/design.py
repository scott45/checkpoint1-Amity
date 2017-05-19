__author__ = 'scotty'

import click
# sys gives access to other variables used by python interpreters
import sys
# colorama, colored terminal text
from colorama import init
# termcolor, Color formatting for output in terminal.
# cprint is a small and simple python library which gives you the possibility to print in color.
from termcolor import cprint
# pyfiglet, takes ASCII text and renders it in ASCII art fonts
from pyfiglet import figlet_format


def app_intro():
    click.secho('!' * 40, fg='yellow')
    click.secho('-' * 40, fg='red')
    init(strip=not sys.stdout.isatty())  # # strip colors if stdout is redirected
    cprint(figlet_format('Amity room allocation', font='big'), 'cyan')
    click.secho('-' * 40, fg='red')
    click.secho('!' * 40, fg='yellow')


def intro_msg():
    click.secho(
        """
    """""""""""'Add people, rooms and have automatic allocations'"""""""""
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



def exit_bar():
    with click.progressbar(range(1000),
                           label=click.secho(
                               'THANKS FOR USING AMITY',
                               blink=True, bold=True),
                           fill_char=click.style('  ', bg='yellow')) as bar:
        for i in bar:
            pass
