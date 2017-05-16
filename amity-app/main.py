__author__ = 'scotty'

"""
TIA -This is Amity!
Usage:
    create_room (L|O) <room_name>...
    add_person <first_name> <last_name> <person_label> [--accommodate=N]
    reallocate_person <qualifier> <new_room_name>
    reallocate_unallocated <qualifier> <new_room_name>
    load_people <filename>
    print_allocations [--o=filename]
    print_unallocated [--o=filename]
    print_room <room_name>
    save_state [--db=sqlite_database]
    load_state <sqlite_database>
    (-i | --interactive)
Options:
    -h --help     Show this screen.
    -v --version
"""

import os
import click
import cmd
from docopt import docopt, DocoptExit

import design

from amity import Amity

design.app_intro()
design.intro_header()
design.exit_bar()
amity = Amity()


def parse(func):
    """
    Essentially a decorator that simplifies the try/except block relays result
    of the docopt parsing to the called action.
    i.e @args_cmd thereafter.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # Throws an Invalid Command message when arguments
            # do not match what is outlined in the __doc__ string.
            msg = 'Invalid Command'
            print(msg)
            print(e)
            return

        except SystemExit:
            # Show help
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


def start():
    design.app_intro()
    design.intro_header()
    arguments = __doc__
    print(arguments)


amity = Amity()


class Interactive_Scott(cmd.Cmd):
    prompt = '(Amity)>> '

    @parse
    def do_create_room(self, args):
        """Usage: create_room <room_type> <room_name>...
        """
        try:
            for r in args['<room_name>']:
                amity.create_room(args['<room_type>'], r)
        except Exception:
            msg = 'An error when running this command'
            click.secho(msg, fg='red', bold=True)

    @parse
    def do_add_person(self, args):
        """Usage: add_person <first_name> <other_name> <person_type> [--accomodate=N] """
        if args['--accommodate'] is None:
            args['--accommodate'] = 'N'
        else:
            args['--accommodate'] = args['--accommodate']

        try:
            validated_details = amity.validate_person(args['<first_name>'],
                                                      args['<other_name>'],
                                                      args['<person_label>'],
                                                      args['--accommodate'])
            if type(validated_details) == list:
                person = amity.generate_identifier(validated_details)
                amity.allocate_room(person)
        except Exception as e:
            print(e)
            msg = 'An error when running this command'
            click.secho(msg, fg='red', bold=True)

    @parse
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <person_id> <room_name>"""
        amity.reallocate_person(args['<person_id>'], args['<room_name>'])

    @parse
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""
        amity.print_room(args['<room_name>'])

    @parse
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=filename]"""
        filename = args['--o']
        if filename:
            amity.print_allocations(filename)
        else:
            amity.print_allocations()

    @parse
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=filename]"""
        filename = args['--o']
        if filename:
            amity.print_unallocated(filename)
        else:
            amity.print_unallocated()

    @parse
    def do_load_people(self, args):
        """Usage: load_people <filename>"""

        if os.path.exists(args['<filename>']):
            filename = args['<filename>']
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    person_details = line.split()
                    if len(person_details) == 3:
                        first_name = person_details[0]
                        other_name = person_details[1]
                        person_label = person_details[2]
                        accommodate = "N"
                        validated_details = amity.validate_person(first_name=first_name,
                                                                  other_name=other_name,
                                                                  person_label=person_label,
                                                                  accommodate=accommodate)
                        if type(validated_details) == list:
                            person = amity.generate_qualifier(
                                validated_details)
                            amity.allocate_room(person)
                    elif len(person_details) == 4:
                        first_name = person_details[0]
                        other_name = person_details[1]
                        person_label = person_details[2]
                        accommodate = person_details[3]
                        validated_details = amity.validate_person(first_name=first_name,
                                                                  other_name=other_name,
                                                                  person_label=person_label,
                                                                  accommodate=accommodate)
                        if type(validated_details) == list:
                            person = amity.generate_qualifier(
                                validated_details)
                            amity.allocate_room(person)
                    else:
                        print("An error occurred")
        else:
            click.secho('Please input a valid name of the file.',
                        fg='red', bold=True)

    @parse
    def do_get_qualifier(self, args):
        """ Usage: get_identifier <first_name> <last_name> """
        first_name = args['<first_name>']
        last_name = args['<last_name>']
        amity.get_qualifier(first_name, last_name)

    @parse
    def do_reallocate_unallocated(self, args):
        """ Usage: reallocate_unallocated <person_id> <room_name> """
        amity.reallocate_unallocated(args['<person_id>'], args['<room_name>'])

    @parse
    def do_save_state(self, args):
        """ Usage: save_state [--db=sqlite_database]"""
        db = args['--db']
        if db:
            amity.save_state(db)
        else:
            amity.save_state()

    @parse
    def do_load_state(self, args):
        """ Usage: save_state <sqlite_database>"""
        try:
            amity.load_state(args['<sqlite_database>'])
            click.secho('Database successfully loaded onto the system',
                        fg='cyan', bold=True)
        except Exception:
            click.secho('Error occurred, please provide valid inputs',
                        fg='red', bold=True)

    @parse
    def do_quit(self, args):
        """Usage: quit """
        design.exit_bar()
        exit()


if __name__ == '__main__':
    try:
        start()
        Interactive_Scott().cmdloop()
    except KeyboardInterrupt:
        design.exit_bar()
