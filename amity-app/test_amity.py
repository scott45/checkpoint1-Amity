__author__ = 'scotty'

import os

import unittest
from amity import Amity

from mock import patch


# tests all functionality of amity class in there defined methods
class TestAmityFunctionality(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    # tests that the class is clean and holds nothing at the time its called
    def test_amity_class_initialises_empty(self):
        self.assertEquals(len(self.amity.rooms), 0)
        self.assertEquals(len(self.amity.people), 0)
        self.assertEquals(len(self.amity.fellows), 0)
        self.assertEquals(len(self.amity.staff), 0)

    # tests the string input is correct
    def test_returns_error_when_non_string_submitted(self):
        self.assertEqual(self.amity.create_room(
            0, 2), 'ValueError. Invalid input',
            msg='Inputs must be of string type')
        self.assertEqual(self.amity.create_room('G', 'Glow'),
                         'Error. Invalid room type input.',
                         msg='Input O or L for room type.')

    # tests that a room is successfully created
    def test_create_room_functionality(self):
        with patch("amity-app.rooms.room.Office"):
            self.amity.create_room("o", "uganda")
            self.assertIn("uganda", self.amity.offices['available'])
        with patch("amity-app.rooms.room.LivingSpace"):
            self.amity.create_room('l', 'kenya')
            self.assertIn('kenya', self.amity.living_spaces['available'])

    # tests that rooms number is increased by one after a room is added
    def test_create_room_list_increments_by_one(self):
        rooms_before = len(self.amity.rooms)
        with patch("amity-app.rooms.room.Office"):
            self.amity.create_room("o", "uganda")
            rooms_after = len(self.amity.rooms)
            self.assertEquals((rooms_after - rooms_before), 1)
            self.amity.create_room('o', 'kenya')
            rooms_after_next = len(self.amity.rooms)
            self.assertAlmostEquals(
                (rooms_after_next - rooms_before), 2)

    # tests that a room can't be created twice
    def test_living_space_cant_be_created_twice(self):
        with patch('amity-app.rooms.room.LivingSpace'):
            self.amity.create_room('l', 'php')
            db = self.amity.create_room('l', 'php')
            self.assertEqual(db, 'php already exists.')

    # tests that an office can only be created once
    def test_office_can_only_be_created_once(self):
        with patch('amity-app.rooms.room.Office'):
            self.amity.create_room('o', 'krypton')
            db2 = self.amity.create_room('o', 'krypton')
            self.assertEqual(db2, 'krypton already exists.')

    # tests that when a  room is created, user is notified
    def test_room_creation_when_successful(self):
        with patch('amity-app.rooms.room.Office'):
            prints = self.amity.create_room('o', 'tsavo')
            self.assertEqual(prints, 'Room tsavo created.')
        with patch('amity-app.rooms.room.LivingSpace'):
            prints = self.amity.create_room('l', 'java')
            self.assertEqual(prints, 'Room java created.')

    # tests to display no rooms have been created
    def test_returns_no_allocations_if_no_rooms_created(self):
        self.assertEqual(self.amity.print_allocations(),
                         '404 No rooms have been created yet to contain allocations.')

    # tests that when a person is created without creating rooms, it will trigger an error
    def test_returns_error_if_no_rooms_created_in_system(self):
        prints = self.amity.validate_person('scott', 'businge', 'Fellow', 'Y')
        self.assertEqual(prints, 'currently no rooms in the system.')

    # tests that a persons names are validated
    def test_validation_of_people_names(self):
        self.amity.create_room('o', 'tent')
        feeds = self.amity.validate_person('scott', 5, 'Fellow', 'y')
        self.assertTrue(feeds)
        self.assertEqual(feeds, 'invalid name inputs.')
        feedss = self.amity.validate_person('ja3sk9900', 'onyango', 'Fellow', 'Y')
        self.assertTrue(feedss)
        self.assertEqual(feedss, 'Names should be of string type')

    # tests that a person's label is right
    def test_validation_of_people_labels(self):
        self.amity.create_room('o', 'camelot')
        res = self.amity.validate_person('mukiibi', 'david', 'tourist', 'y')
        self.assertTrue(res)
        self.assertEqual(res, 'tourist is an invalid Person label. it can either be staff or fellow')

    # tests that accomodation input is either y or n
    def test_wants_accomodation_is_only_y_or_n(self):
        self.amity.create_room('o', 'orange')
        prints = self.amity.validate_person(
            'daisy', 'macharia', 'Fellow', 'No')
        self.assertTrue(prints)
        self.assertEqual(prints, 'Input must either be Y or N')

    # tests that validation is correct but missing an office
    def test_validation_if_person_fellow_and_wants_accommodation(self):
        self.amity.create_room('o', 'tent3')
        prints = self.amity.validate_person('tumbo', 'kevin', 'Fellow', 'Y')
        self.assertTrue(prints)
        self.assertEqual(prints, 'No Living space for kevin.')

    # tests that validation is correct
    def test_validation_if_submissions_are_right(self):
        self.amity.create_room('l', 'scala')
        self.amity.create_room('o', 'tent2')
        prints = self.amity.validate_person('timothy', 'wikedzi', 'Fellow', 'y')
        person = self.amity.generate_qualifier(prints)
        self.amity.allocate_room(person)
        for room in self.amity.rooms:
            if room.room_name == 'scala':
                self.assertIn('timothy wikedzi', room.occupants)
                self.assertEqual(len(room.occupants), 1)
            if room.room_name == 'tent2':
                self.assertIn('timothy wikedzi', room.occupants)
                self.assertEqual(len(room.occupants), 1)

    # tests that objects are created
    def test_person_objects_are_created(self):
        self.amity.create_room('o', 'tent4')
        self.amity.create_room('l', 'html')
        prints = self.amity.validate_person('kitui', 'daniel', 'Fellow', 'y')
        person = self.amity.generate_qualifier(prints)
        for person in self.amity.people:
            if person.full_name == 'kitui daniel':
                self.assertEqual(person.person_type, 'Fellow')
                self.assertEqual(person.identifier, 'F1')

        prints= self.amity.validate_person('taracha', 'rogers', 'Staff', 'n')
        person = self.amity.generate_identifier(prints)
        for person in self.amity.people:
            if person.full_name == 'taracha rogers':
                self.assertEqual(person.person_type, 'Staff')
                self.assertEqual(person.identifier, 'S1')

    # tests qualifier error is generated if no people
    def test_get_qualifier_if_no_people_created(self):
        self.assertEqual(self.amity.get_qualifier(
            'scott', 'businge'), 'you havent created people yet')

    # tests qualifier is generated if people are added
    def test_get_qualifier_if_people_created(self):
        self.amity.create_room('o', 'tent5')
        self.amity.create_room('l', 'ruby')
        prints = self.amity.validate_person('waithera', 'doris', 'Fellow', 'y')
        res = self.amity.generate_qualifier(prints)
        self.assertEqual(self.amity.get_identifier(
            'waithera', 'doris'), 'F1')

    # tests reallocation functionality
    def test_reallocate_someone(self):
        self.amity.create_room('o', 'tent6')
        self.amity.create_room('o', 'tent7')
        prints = self.amity.validate_person('driver', 'papa', 'staff', 'n')
        person = self.amity.generate_qualifier(prints)
        self.amity.allocate_room(person)
        yah = self.amity.reallocate_person('r.13', [])
        self.assertEqual(yah, "Error... invalid room data-type.")

    # tests reallocation on wrong room name
    def test_reallocate_person_when_room_uncreated(self):
        self.amity.create_room('o', 'tent8')
        self.amity.create_room('o', 'tent9')
        prints = self.amity.validate_person('marion', 'food', 'staff', 'n')
        person = self.amity.generate_qualifier(prints)
        self.amity.allocate_room(person)
        respond = self.amity.reallocate_person('S1', 'tent10')
        self.assertEqual(respond, "unknown room name.")

    # tests reallocation without desiring accommodation
    def test_reallocate_person_when_person_accomodate_is_N(self):
        self.amity.create_room('o', 'tsavo2')
        self.amity.create_room('l', 'swift')
        prints = self.amity.validate_person('victoria', 'Auka', 'Fellow', 'n')
        person = self.amity.generate_identifier(prints)
        self.amity.allocate_room(person)
        respond = self.amity.reallocate_person('F1', 'victoria')
        self.assertEqual(respond, 'Accommodation isnt needed by this fellow')
        for room in self.amity.rooms:
            if room.room_name == 'swift':
                self.assertNotIn('victoria Auka', room.occupants)

    # tests that reallocation to the same room raises an error
    def test_reallocate_to_same_room(self):
        self.amity.create_room('o', 'tsavo3')
        res = self.amity.validate_person('dominic', 'motuka', 'Fellow', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        res = self.amity.reallocate_person('F1', 'tsavo3')
        self.assertEqual(res, 'reallocation to same room not possible')

    # tests that when a  room is created, user is notified
    def test_reallocate_to_same_room_if_person_id_non_exitent(self):
        self.amity.create_room('o', 'Mars')
        self.amity.create_room('o', 'Venus')
        res = self.amity.validate_person(
            'serallynnette', 'wanjiku', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        res = self.amity.reallocate_person('Staff1', 'Mars')
        self.assertEqual(res, 'Invalid person id.')

    def test_reallocate_person_works(self):
        self.amity.create_room('o', 'valhalla')
        res = self.amity.validate_person(
            'seralynnette', 'wanjiku', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        self.amity.create_room('o', 'narnia')
        res = self.amity.reallocate_person('S1', 'narnia')
        self.assertEqual(res, 'Person reallocated to Narnia')
        for room in self.amity.rooms:
            if room.room_name == 'Valhalla':
                self.assertNotIn('Seralynnette Wanjiku', room.occupants)
            if room.room_name == 'Narnia':
                self.assertIn('Seralynnette Wanjiku', room.occupants)

    def test_reallocate_unallocated(self):
        self.amity.create_room('o', 'prayar')
        res = self.amity.validate_person('Austin', 'Mugage', 'staff')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        res = self.amity.reallocate_unallocated('s65', 'Prayar')
        self.assertEqual(res, 'Person ID does not exist.')

    def test_print_room_if_no_rooms(self):
        res = self.amity.print_room('Jupite')
        self.assertEqual(res, 'No rooms exist at the moment.')

    def test_if_room_exists(self):
        self.amity.create_room('o', 'jupite')
        res = self.amity.print_room('SOHK')
        self.assertEqual(res, 'Room does not exist.')

    def test_print_unallocated_if_all_allocated(self):
        self.amity.create_room('o', 'lyon')
        res = self.amity.validate_person('Lyon', 'Witherspoon', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        res = self.amity.print_unallocated()
        self.assertEqual(res, 'No unallocated people as per now.')

    def test_print_unallocated_if_exisiting(self):
        self.amity.create_room('o', 'Witherspoon')
        res = self.amity.validate_person('Lyon', 'Witherspoon', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        self.amity.unallocated_persons.append('Person Name')
        res = self.amity.print_unallocated()
        self.assertTrue(res, 'Some people unallocated.')

    def test_save_state(self):
        self.amity.create_room('o', 'Witherspoon')
        res = self.amity.validate_person('Lyon', 'Witherspoon', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        self.assertFalse(os.path.exists('default_db_self.amity.sqlite'))

    def save_state_works(self):
        self.amity.create_room('o', 'Witherspoon')
        res = self.amity.validate_person('Lyon', 'Witherspoon', 'Staff', 'n')
        person = self.amity.generate_identifier(res)
        self.amity.allocate_room(person)
        res = self.amity.save_state()
        self.assertEqual(res, True)

