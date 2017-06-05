from random import randint

__author__ = 'scotty'

import os
import time
import click

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
        self.people = []
        self.f_ids = [0]
        self.s_ids = [0]
        self.staff_allocations = []
        self.fellow_allocations = []
        self.unallocated_persons = []

    # instatiates rooms as instances of the amity class clearly ensuring validated inputs
    def create_room(self, room_type, room_name):
        if type(room_type) != str or room_type.upper() not in ['O', 'L']:
            click.secho('Invalid input, please enter O or L for a room type.',
                        fg='red', bold=True)
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
                            fg='cyan', bold=True)
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
                    output += occupant + "\n"
                    # output += '\n'
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
            return 'Print to screen'

    # validates the add person functionality
    def validate_person(self, first_name, other_name, person_label,
                        accommodate='N'):
        if type(first_name) != str or type(other_name) != str:
            click.secho('Incorrect data type input.', fg='red', bold=True)
            return 'input-Error, name should be string'
        if not first_name.isalpha() or not other_name.isalpha():
            click.secho('Names must be in alphabetical strings',
                        fg='red', bold=True)
            return 'Non-Alphabetical names added'
        if person_label.title() not in ['Fellow', 'Staff']:
            click.secho('Please enter either Fellow or Staff for person label',
                        fg='red', bold=True)
            return 'Invalid Person label'
        if accommodate.upper() not in ('Y', 'N'):
            click.secho('Please Enter Y or N for accommodation option.',
                        fg='red', bold=True)
            return 'Input-Error, accommodation option not Y or N'
        accommodate = accommodate.upper()
        person_label = person_label.title()
        if person_label.title() == 'Staff' and accommodate == 'Y':
            accommodate = 'N'
            click.secho(
                'Staff not given accommodation. only an office is allocated.',
                fg='red', bold=True)
        all_names = first_name.title() + ' ' + other_name.title()
        for person in self.people:
            if person.all_names == all_names and \
                            person.person_label == person_label.title():
                click.secho('%s %s Already Exists.' % (person_label, all_names))
                return 'This Person exists.'
        for person in self.people:
            if not self.offices['available'] and person_label == 'Staff':
                self.unallocated_persons.append(person.all_names)
                click.secho(
                    'No offices to be allocated into currently.',
                    fg='red', bold=True)
                return 'There are no offices created currently.'
            if not self.living_spaces['available'] and not \
                    self.offices['available']:
                self.unallocated_persons.append(person.all_names)
                click.secho(
                    'Create room first to add person. Not any room (office or living space)'
                    ' has been created in the system yet.',
                    fg='red', bold=True)
                return 'There are no rooms in the system.'

            if accommodate == 'Y' and person_label == 'Fellow':
                if not self.living_spaces['available']:
                    self.unallocated_persons.append(person.all_names)
                    output = 'Add a living space for this fellow '
                    output += 'to be allocated both.'
                    click.secho(output, fg='red', bold=True)
                    return 'No Living space for fellow to be allocated into.'
                elif not self.offices['available']:
                    self.unallocated_persons.append(person.all_names)
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
                self.people.append(person)
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
        time.sleep(1)
        if person.person_label == 'Staff':
            staff_single_allocation = {}
            staff_single_allocation[person.all_names] = self.offices['available'][
                randint(0, (len(self.offices['available']) - 1))]
            self.staff_allocations.append(staff_single_allocation)
            for room in self.rooms:
                if room.room_name == staff_single_allocation[person.all_names]:
                    if room.capacity > 0:
                        click.secho('Allocation successful!', fg='green')
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
                fellow_single_allocation = {}
                fellow_single_allocation['all_name'] = person.all_names
                fellow_single_allocation['office'] = self.offices['available'][
                    randint(0, (len(self.offices['available']) - 1))]
                fellow_single_allocation['living_space'] = self.living_spaces['available'][
                    randint(0, (len(self.living_spaces['available']) - 1))]
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
                fellow_single_allocation = {}
                fellow_single_allocation[person.all_names] = \
                    self.offices['available'][
                        randint(0, (len(self.offices['available']) - 1))]
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
                if person.all_names == fn:
                    output = click.secho(person.qualifier, fg='green')
                    return person.qualifier
            else:
                output = click.secho('The person does not exist.', fg='white')
                return output

    # method that prints a room
    def print_room(self, room_name):
        if not self.rooms:
            click.secho('No rooms have been created yet.',
                        fg='cyan', bold=True)
            return 'No rooms exist currently.'
        all_rooms = []
        for room in self.rooms:
            all_rooms.append(room.room_name)
        if room_name.title() not in all_rooms:
            click.secho('The room name %s does not exist in the database.' %
                        room_name, fg='red', bold=True)
            return 'Room does not exist in the system.'

        room_name = room_name.title()
        for room in self.rooms:
            if room.room_name == room_name:
                click.secho('ROOM NAME:%s(%s)' %
                            (room_name, room.room_type),
                            fg='green', bold=True)
                click.secho('=' * 10, fg='white')
                if room.occupants:
                    for occupant in room.occupants:
                        click.secho(occupant, fg='cyan')
                else:
                    click.secho('No body has been allocated in here.', fg='cyan', bold=True)
                    return False

    # function to implement reallocation process
    def reallocate_person(self, person_id, room_name):
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
            if person.all_names in self.unallocated_persons and person.qualifier == person_id:
                click.secho('person wasnt allocated a room before, use command reallocate unallocated',
                            fg='red', bold=True)
                return 'unallocated person.'
        if room_name.title() not in available_rooms:
            click.secho('Room name %s does not exist.' %
                        room_name, fg='white', bold=True)
            return 'Room does not exist.'
        for person in self.people:
            if person.accommodate == 'N' and person.qualifier == person_id:
                if room_name in self.living_spaces['available']:
                    click.secho(
                        'system cannot move person from office to living space',
                        fg='red', bold=True)
                    return 'Fellow does not want to have accommodation here'
        all_person_ids = []
        for person in self.people:
            all_person_ids.append(person.qualifier)
            if person.qualifier == person_id:
                person_name = person.all_names
        if person_id not in all_person_ids:
            click.secho('Person ID entered does not exist.',
                        fg='white', bold=True)
            return "Invalid person id."
        for person in self.people:
            if person.qualifier == person_id:
                desired = person.all_names
        for room in self.rooms:
            if desired in room.occupants and \
                            room.room_name == room_name:
                click.secho('You cannot be reallocated to the same room you were given at first.',
                            fg='red', bold=True)
                return 'Cant reallocate a person to same room'
        if room_name in self.offices['available']:
            room_state = 'Office'
        if room_name in self.living_spaces['available']:
            room_state = 'Living Space'
        for room in self.rooms:
            if person_name in room.occupants and room_state == room.room_type:
                new_room = room.room_name
                room.occupants.remove(person_name)
        for room in self.rooms:
            if room.room_name == room_name and room.capacity > 0:
                room.capacity = room.add_person(person_name)
                click.secho('%s has been moved from %s to %s.' %
                            (person_name, new_room, room.room_name),
                            fg='green', bold=True)
                return 'Person moved to %s' % room_name

    # Reallocate someone who is in the unallocated section
    def reallocate_unallocated(self, person_id, room_name):
        available_rooms = []
        if type(room_name) != str:
            return 'Error. Enter valid room name of string type.'
        room_name = room_name.title()
        person_id = person_id.upper()
        people_ids = []
        for person in self.people:
            people_ids.append(person.qualifier)
        if person_id not in people_ids:
            click.secho('Person ID does not exist', fg='white', bold=True)
            return 'Person ID entered does not exist.'

        for room in self.offices['available']:
            available_rooms.append(room)
        for room in self.living_spaces['available']:
            available_rooms.append(room)
        if room_name.title() not in available_rooms:
            click.secho('Room name %s does not exist in the allocations ready room.' %
                        room_name, fg='white', bold=True)
            return 'Room does not exist in the list.'
        for person in self.people:
            if person.all_names in self.unallocated_persons and \
                            person.qualifier == person_id:
                unallocated_person = person.all_names
        for room in self.rooms:
            if room.room_name == room_name:
                room.occupants.append(unallocated_person)
                self.unallocated_persons.remove(unallocated_person)
                click.secho('%s moved to %s' % (
                    unallocated_person, room_name), fg='green', bold=True)

    # people who havent been allocated rooms
    def print_unallocated(self, filename=None):
        if not self.unallocated_persons:
            click.secho('There is no unallocated person currently.',
                        fg='cyan', bold=True)
            return 'No unallocated person.'
        else:
            click.secho('Unallocated people in the system.',
                        fg='green', bold=True)
            print(self.unallocated_persons)

            for unallocated in self.unallocated_persons:
                click.secho(unallocated, fg='cyan')
        if filename:
            file = open(filename + '.txt', 'w')
            file.write("Unallocated people in the system.")
            file.write('\n')
            for unallocated in self.unallocated_persons:
                file.write(unallocated)
                file.write('\n')
            click.secho('List stored in %s.txt' % filename, fg='cyan')

    # test save state functionality
    def save_state(self, db_name=None):
        if os.path.exists('amity_db.sqlite'):
            os.remove('amity_db.sqlite')
        if db_name is None:
            db = DatabaseManager()
        else:
            db = DatabaseManager(db_name)
        Base.metadata.bind = db.engine
        s = db.session()
        try:
            for person in self.people:
                for room in self.rooms:
                    if person.all_names in room.occupants:
                        if room.room_type == 'Office':
                            office_allocated = room.room_name
                        if room.room_type == 'Living Space' and \
                                person.accommodate == 'Y':
                            ls_allocated = room.room_name
                        else:
                            ls_allocated = None
                    if person.all_names in self.unallocated_persons:
                        ls_allocated = 'Unallocated'
                        office_allocated = 'Unallocated'
                saved_data = People(
                    person_qualifier=person.qualifier,
                    person_name=person.all_names,
                    person_label=person.person_label,
                    wants_accommodation=person.accommodate,
                    office_allocated=office_allocated,
                    living_space_allocated=ls_allocated
                )
                s.merge(saved_data)

            for room in self.rooms:
                room_to_db = Rooms(
                    room_name=room.room_name,
                    room_type=room.room_type,
                    room_capacity=room.capacity,
                )
                s.merge(room_to_db)
            s.commit()
            output = "the Data has successfully been added to {} database". \
                format(db.db_name.upper())
            click.secho(output, fg='cyan', bold=True)
            return True
        except Exception as e:
            print(e)
            return True

    # load state method
    def load_state(self, db_name):
        engine = create_engine('sqlite:///' + db_name + '.sqlite')
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        all_people = session.query(People).all()
        all_rooms = session.query(Rooms).all()
        for r in all_rooms:
            if r.room_type == 'Office':
                room = Office(r.room_name)
                if r.room_capacity > 0:
                    self.offices['available'].append(r.room_name)
                else:
                    self.offices['unavailable'].append(r.room_name)
            elif r.room_type == 'Living Space':
                room = LivingSpace(r.room_name)
                if r.room_capacity > 0:
                    self.living_spaces['available'].append(r.room_name)
                else:
                    self.living_spaces['unavailable'].append(r.room_name)
            self.rooms.append(room)
        for p in all_people:
            if not self.people:
                if p.person_label == 'Fellow':
                    all_names = p.person_name.split()
                    person = Fellow(all_names[0], all_names[1])
                    f_id = 1
                    self.f_ids.append(f_id)
                    qualifier = 'F' + str(f_id)
                    person.qualifier = qualifier
                    person.accommodate = p.wants_accommodation
                    person.get_all_names()
                    self.fellows.append(person.all_names)
                elif p.person_label == 'Staff':
                    all_names = p.person_name.split()
                    person = Staff(all_names[0], all_names[1])
                    s_id = 1
                    self.s_ids.append(s_id)
                    qualifier = 'S' + str(s_id)
                    person.qualifier = qualifier
                    person.accommodate = p.wants_accommodation
                    person.get_all_names()
                    self.staff.append(person.all_names)
            else:
                if p.person_label == 'Fellow':
                    all_names = p.person_name.split()
                    person = Fellow(all_names[0], all_names[1])
                    f_id = self.f_ids.pop() + 1
                    qualifier = 'F' + str(f_id)
                    self.f_ids.append(f_id)
                    person.accommodate = p.wants_accommodation
                    person.qualifier = qualifier
                    person.get_all_names()
                    self.fellows.append(person.all_names)
                elif p.person_label == 'Staff':
                    all_names = p.person_name.split()
                    person = Staff(all_names[0], all_names[1])
                    s_id = self.s_ids.pop() + 1
                    qualifier = 'S' + str(s_id)
                    person.identifier = qualifier
                    self.s_ids.append(s_id)
                    person.accommodate = p.wants_accommodation
                    person.get_all_names()
                    self.fellows.append(person.all_names)
            self.people.append(person)
            # Append person object to people list.
            for room in self.rooms:
                if p.living_space_allocated == room.room_name:
                    room.add_person(p.person_name)
                if p.office_allocated == room.room_name:
                    room.add_person(p.person_name)
            if p.office_allocated == 'Unallocated':
                self.unallocated_persons.append(p.person_name)
        return 'Db finished loading!!.'

    def delete_person(self, first_name, other_name):
        if type(first_name) != str or type(other_name) != str:
            click.secho('Incorrect data type input.', fg='red', bold=True)
            return 'input-Error, name should be string'

        if not first_name.isalpha() or not other_name.isalpha():
            click.secho('Names must be in alphabetical strings',
                        fg='red', bold=True)
            return 'Non-Alphabetical names added'

        for person in self.people:
            if person.all_names not in self.fellows:
                msg = "Person {} does not exist!".format(person.all_names)
                print(person.all_names)
                click.secho(msg, bold=True, fg='red')
                return msg
            else:
                for room in self.rooms:
                    for occupant in room.occupants:
                        if person == room.occupants:
                            self.delete_person(occupant)
                            person.is_active = False
                for person in self.unallocated_persons:
                    if person.all_names == int(person.person_id):
                        action = self.unallocated_persons.index(person)
                        del self.unallocated_persons[action]
                if person.all_names == person.all_names:
                    indx = self.people.index(person)
                    del self.people[indx]
                    person.is_active = False
                    msg = "person {} has been successfully deleted" \
                        .format(person.all_names)
                    click.secho(msg, bold=True, fg='green')
                    return msg

    def delete_room(self, room_type, room_name):
        if type(room_type) != str or room_type.upper() not in ['O', 'L']:
            click.secho('Invalid input, please enter O or L for a room type.',
                        fg='red', bold=True)
            return 'Input-Error. Invalid room type input.'
        if type(room_name) != str:
            click.secho('Incorrect data type input.', fg='red', bold=True)
            return 'input-Error, name should be string'
        if not room_name.isalpha():
            click.secho('Room names must be in alphabetical strings',
                        fg='red', bold=True)
            return 'Non-Alphabetical names added'
        room_type = room_type.strip().upper()
        room_name = room_name.strip().title()
        if room_type == 'O':
            room_type = 'Office'
        if room_type == 'L':
            room_type = 'Living Space'
        for room in self.rooms:
            if room_type == 'Office':
                room = Office(room_name)
                if room_name not in self.offices['available'] or room_name not in self.living_spaces['available']:
                    msg = "Room {} does not exist!".format(room_name)
                    click.secho(msg, bold=True, fg='red')
                    return msg
            else:
                if room_name == room.room_name:
                    if room.occupants:
                        for occupant in room.occupants:
                            self.unallocated_persons.append(occupant)
                        room.occupants = []
                    indx = self.rooms.index(room)
                    del self.rooms[indx]

                    room.in_use = False
                    msg = "Room {} has been successfully deleted" \
                        .format(room_name)
                    click.secho(msg, bold=True, fg='green')
                    return msg
