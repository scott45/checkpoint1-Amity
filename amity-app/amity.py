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
