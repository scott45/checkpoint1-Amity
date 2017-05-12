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

    # tests that when a  room is created, user is notified
    def test_validation_if_person_fellow_and_wants_accomodation(self):
        pass

    # tests that when a  room is created, user is notified
    def test_passes_validation_and_creates_person(self):
        pass

    # tests that when a  room is created, user is notified
    def test_person_objects_are_created(self):
        pass

    # tests that when a  room is created, user is notified
    def test_get_identifier_if_no_people_added(self):
        pass

    # tests that when a  room is created, user is notified
    def test_get_identifier_if_people_added(self):
        pass

    # tests that when a  room is created, user is notified
    def test_reallocate_person(self):
        pass

    # tests that when a  room is created, user is notified
    def test_reallocate_person_when_room_does_not_exist(self):
        pass

    # tests that when a  room is created, user is notified
    def test_reallocate_person_when_person_accomodate_is_N(self):
        pass

    # tests that when a  room is created, user is notified
    def test_reallocate_to_same_room(self):
        pass

    # tests that when a  room is created, user is notified
    def test_reallocate_to_same_room_if_person_id_non_exitent(self):
        pass

    def test_reallocate_person_works(self):
        pass

    def test_reallocate_unallocated(self):
        pass

    def test_print_room_if_no_rooms(self):
        pass

    def test_if_room_exists(self):
        pass

    def test_print_unallocated_if_all_allocated(self):
        pass

    def test_print_unallocated_if_exisiting(self):
        pass

    def test_save_state(self):
        pass

    def save_state_works(self):
        pass

    def test_returns_correct_message(self):
        pass

    def test_database_loaded(self):
        pass
