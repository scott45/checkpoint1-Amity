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
            if person.all_names == all_names and \
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

    # function for generating a persons own identifier
    def generate_qualifier(self, validated_details):
        all_names = validated_details[0]
        accommodate = validated_details[1]
        person_label = validated_details[2]
        all_namess = all_names.split()
        if not self.people:
            if person_label.title() == 'Fellow':
                f_id = 1
                self.f_ids.append(f_id)
                identifier = 'F' + str(f_id)
                person = Fellow(all_namess[0], all_namess[1])
                person.accommodate = accommodate
                person.get_all_names()
                person.assign_qualifier(identifier)
                self.fellows.append(person.all_names)
            elif person_label.title() == 'Staff':
                s_id = 1
                self.s_ids.append(s_id)
                identifier = 'S' + str(s_id)
                person = Staff(all_namess[0], all_namess[1])
                person.accommodate = accommodate
                person.get_all_names()
                person.assign_qualifier(identifier)
                self.staff.append(person.all_names)
        else:
            if person_label.title() == 'Fellow':
                person = Fellow(all_namess[0], all_namess[1])
                person.accommodate = accommodate
                person.get_all_names()
                f_id = self.f_ids.pop() + 1
                identifier = 'F' + str(f_id)
                self.f_ids.append(f_id)
                person.assign_qualifier(identifier)
                self.fellows.append(person.all_names)
            elif person_label.title() == 'Staff':
                person = Staff(all_namess[0], all_namess[1])
                person.accommodate = accommodate
                person.get_all_names()
                s_id = self.s_ids.pop() + 1
                identifier = 'S' + str(s_id)
                self.s_ids.append(s_id)
                person.assign_qualifier(identifier)
                self.fellows.append(person.all_names)
        self.people.append(person)
        click.secho('The %s %s has been created.\n' %
                    (person.person_label, person.all_names),
                    fg='green', bold=True)
        return person

    # allocating a room
    def allocate_room(self, person):
        click.secho('room allocation in progress....', fg='green')
        time.sleep(2)
        if person.person_label == 'Staff':
            staff_single_allocation = {person.all_names: self.offices['available'][
                randint(0, (len(self.offices['available']) - 1))]}
            self.staff_allocations.append(staff_single_allocation)
            for room in self.rooms:
                if room.room_name == staff_single_allocation[person.all_names]:
                    if room.capacity > 0:
                        click.secho('Success!', fg='green')
                        room.capacity = room.add_person(person.all_names)
                    else:
                        self.offices['available'].remove(room.room_name)
                        self.offices['unavailable'].append(room.room_name)
                        self.unallocated_persons.append(person.all_names)
                        msg = '%s has reached full capacity.' % room.room_name
                        msg += 'add another %s.' % room.room_type
                        click.secho(msg, fg='red', bold=True)

        if person.person_label == 'Fellow':
            if person.accommodate == 'Y':
                fellow_single_allocation = {'name': person.all_names, 'office': self.offices['available'][
                    randint(0, (len(self.offices['available']) - 1))], 'living_space': self.living_spaces['available'][
                    randint(0, (len(self.living_spaces['available']) - 1))]}
                self.fellow_allocations.append(fellow_single_allocation)
                for room in self.rooms:
                    if room.room_name == fellow_single_allocation['office']:
                        if room.capacity > 0:
                            room.capacity = room.add_person(person.all_names)
                        else:
                            self.offices['available'].remove(room.room_name)
                            self.offices['unavailable'].append(room.room_name)
                            self.unallocated_persons.append(person.all_names)
                            msg = '%s has reached its Maximum capacity.' % room.room_name
                            msg += 'Please add another %s.' % room.room_type
                            click.secho(msg, fg='red', bold=True)
                    elif room.room_name == fellow_single_allocation['living_space']:
                        if room.capacity > 0:
                            room.capacity = room.add_person(person.all_names)
                        else:
                            self.living_spaces[
                                'available'].remove(room.room_name)
                            self.living_spaces[
                                'unavailable'].append(room.room_name)
                            self.unallocated_persons.append(person.all_names)
                            msg = '%s has reached full capacity.' % room.room_name
                            msg += 'Please add another %s.' % room.room_type
                            click.secho(msg, fg='red', bold=True)
                click.secho('Success!', fg='green')
                return 'Allocated both a living space and an office'
            else:
                fellow_single_allocation = {person.all_names: self.offices['available'][
                    randint(0, (len(self.offices['available']) - 1))]}
                self.fellow_allocations.append(fellow_single_allocation)
                for room in self.rooms:
                    if room.room_name == \
                            fellow_single_allocation[person.all_names]:
                        if room.capacity > 0:
                            click.secho('Success!', fg='green')
                            room.capacity = room.add_person(person.all_names)
                        else:
                            self.offices['available'].remove(room.room_name)
                            self.offices['unavailable'].append(room.room_name)
                            self.unallocated_persons.append(person.all_names)
                            msg = '%s has reached full capacity.' % room.room_name
                            msg += 'Please add another %s.' % room.room_type
                            click.secho(msg, fg='red', bold=True)

    # get qualifier for reallocation to enable operation
    def get_qualifier(self, first_name, last_name):
            if not self.people:
                click.secho('No people in the system.')
                return 'No people have been added yet'
            else:
                fn = first_name.title() + ' ' + last_name.title()
                for person in self.people:
                    if person.all_names_name == fn:
                        output = click.secho(person.qualifier, fg='green')
                        return person.qualifier
                else:
                    output = click.secho('The person does not exist.', fg='white')
                    return output

    def reallocate_person(self, person_id, room_name):
        '''
        The beginning of the method validates of the data passed
        is a string and then proceeds to take the person_id and
        accordingly reallocate them.
        PERSON_ID which in this case is the identifier
        is converted to upper case.
        '''
        available_rooms = []
        if type(room_name) != str:
            return 'Error. Please enter valid room name.'
        for room in self.offices['available']:
            available_rooms.append(room)
        for room in self.living_spaces['available']:
            available_rooms.append(room)
        person_id = person_id.upper()
        room_name = room_name.title()
        for person in self.people:
            if person.full_name in self.unallocated_persons and person.identifier == person_id:
                click.secho('Person is not allocated. Please use --->reallocate unallocated',
                            fg='yellow', bold=True)
                return 'unallocated person.'
        if room_name.title() not in available_rooms:
            click.secho('Room name %s does not exist.' %
                        room_name, fg='red', bold=True)
            return 'Room does not exist.'
        for person in self.people:
            if person.accomodate == 'N' and person.identifier == person_id:
                if room_name in self.living_spaces['available']:
                    click.secho(
                        'Cant move person from office to living space',
                        fg='red', bold=True)
                    return 'Fellow does not want accomodation'
        all_person_ids = []
        for person in self.people:
            all_person_ids.append(person.identifier)
            if person.identifier == person_id:
                person_name = person.full_name
        if person_id not in all_person_ids:
            click.secho('Person ID entered does not exist.',
                        fg='red', bold=True)
            return "Invalid person id."
        for person in self.people:
            if person.identifier == person_id:
                wanted_name = person.full_name
        for room in self.rooms:
            if wanted_name in room.occupants and \
                    room.room_name == room_name:
                click.secho('You cannot be reallocated to the same room.',
                            fg='red', bold=True)
                return 'cant reallocate to same room'
        if room_name in self.offices['available']:
            room_t = 'Office'
        if room_name in self.living_spaces['available']:
            room_t = 'Living Space'
        for room in self.rooms:
            if person_name in room.occupants and room_t == room.room_type:
                current_room = room.room_name
                room.occupants.remove(person_name)

        # Reallocate to actual room
        for room in self.rooms:
            if room.room_name == room_name and room.capacity > 0:
                room.capacity = room.add_person(person_name)
                click.secho('%s has been reallocated from %s to %s.' %
                            (person_name, current_room, room.room_name),
                            fg='green', bold=True)
                return 'Person reallocated to %s' % room_name


