__author__ = 'scotty'

import os
import time
import click
from random import randint

from rooms.room import LivingSpace, Office
from people.person import Fellow, Staff
from database.models import People, Rooms, DatabaseManager, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Amity(object):
    def __init__(self):
        self.offices = {
            'available': [],
            'unavailable': []
        }
        self.living_spaces = {
            'available': [],
            'unavailable': []
        }
        self.rooms = []
        self.fellows = []
        self.staff = []
        self.people = self.staff + self.fellows
        self.f_ids = [0]
        self.s_ids = [0]
        self.staff_allocations = []
        self.fellow_allocations = []
        self.unallocated_persons = []

    # instatiates rooms as instances of the amity class clearly ensuring validated inputs
    def create_room(self, room_type, room_name):
        if type(room_type) != str or room_type.upper() not in ['O', 'L']:
            click.secho('Invalid input, please enter O or L for a room type.',
                        fg='white', bold=True)
            return 'Input-Error. Invalid room type input.'
        room_type = room_type.strip().upper()
        room_name = room_name.strip().title()
        if room_type == 'O':
            room_type = 'Office'
        if room_type == 'L':
            room_type = 'Living Space'
        for room in self.rooms:
            if room.room_name == room_name and \
                    room.room_type == room_type:
                click.secho('%s %s already exists, choose another name'
                            % (room_type, room_name),
                            fg='white', bold=True)
                return 'Room already created.'
        if room_type == 'Office':
            room = Office(room_name)
            self.offices['available'].append(room.room_name)
        elif room_type == 'Living Space':
            room = LivingSpace(room_name)
            self.living_spaces['available'].append(room.room_name)
        self.rooms.append(room)
        click.secho('%s %s has been created.' %
                    (room.room_type, room.room_name), bold=True, fg='green')
        return 'Room %s created.' % room.room_name

    # prints allocations with its occupants
    def print_allocations(self, filename=None):
        if not self.rooms:
            click.secho('No rooms created in the system yet.',
                        fg='red', bold=True)
            return 'No rooms have been created yet in the system.'
        output = ''
        for room in self.rooms:
            # print(room.room_name)
            # print(room.occupants)
            output += '**' * 5
            output += '\n'
            output += room.room_name + '(' + room.room_type + ')'
            output += '\n'
            output += '**' * 5
            output += '\n'
            if room.occupants:
                for occupant in room.occupants:
                    output += occupant
                    output += '\n'
            else:
                output += 'No people have been allocated in %s yet.' % room.room_name
                output += '\n'
        if filename is None:
            click.secho(output, fg='cyan')
            return 'Print to screen'

        else:
            file = open(filename + '.txt', 'w')
            file.write(output)
            click.secho('Printed to %s.txt' % filename, fg='green')
            return 'Print to file'

    # validates the add person functionality
    def validate_person(self, first_name, other_name, person_label,
                        accommodate='N'):
        if type(first_name) != str or type(other_name) != str:
            click.secho('Incorrect data type input.', fg='white', bold=True)
            return 'input-Error, name should be string'
        if not first_name.isalpha() or not other_name.isalpha():
            click.secho('Names must be in alphabetical strings',
                        fg='white', bold=True)
            return 'Non-Alphabetical names added'
        if person_label.title() not in ['Fellow', 'Staff']:
            click.secho('Please enter either Fellow or Staff for person type',
                        fg='white', bold=True)
            return 'Invalid Person Type'
        if accommodate.upper() not in ['Y', 'N']:
            click.secho('Please Enter Y or N for accommodation option.',
                        fg='white', bold=True)
            return 'Input-Error, accommodation option not Y or N'
        accommodate = accommodate.upper()
        person_label = person_label.title()
        if person_label == 'Staff' and accommodate == 'Y':
            accommodate = 'N'
            click.secho(
                'Staff not given accommodation. only an office is allocated.',
                fg='white', bold=True)
        all_names = first_name.title() + ' ' + other_name.title()
        for person in self.people:
            if person.full_name == all_names and \
                    person.person_label == person_label.title():
                click.secho('%s %s Already Exists.' % (person_label, all_names))
                return 'This Person exists.'
        if not self.offices['available'] and person_label == 'Staff':
            click.secho(
                'No offices to be allocated into currently.',
                fg='red', bold=True)
            return 'There are no offices created currently.'
        if not self.living_spaces['available'] and not \
                self.offices['available']:
            click.secho(
                'Not any room (office or living space) has been created in the system yet.',
                fg='red', bold=True)
            return 'There are no rooms in the system.'

        if accommodate == 'Y' and person_label == 'Fellow':
            if not self.living_spaces['available']:
                output = 'Add a living space for this fellow '
                output += 'to be allocated both.'
                click.secho(output, fg='red', bold=True)
                return 'No Living space for fellow to be allocated into.'
            elif not self.offices['available']:
                output = 'Add an office for this fellow '
                output += 'to be allocated both .'
                click.secho(output, fg='red', bold=True)
                return 'No office for fellow to be allocated into.'
        return [all_names, accommodate, person_label]
