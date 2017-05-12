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
    def test_amity_class_initialises_with_nothing(self):
        self.assertEquals(len(self.amity.rooms), 0)
        self.assertEquals(len(self.amity.people), 0)
        self.assertEquals(len(self.amity.fellows), 0)
        self.assertEquals(len(self.amity.staff), 0)

    # tests the string input is correct
    def test_returns_error_when_non_string_is_addded(self):
        self.assertEqual(self.amity.create_room(
            0, 2), 'ValueError. Invalid input',
            msg='Inputs must be of string type')
        self.assertEqual(self.amity.create_room('G', 'Glow'),
                         'Error. Invalid room type input.',
                         msg='Input O or L for room type.')

    # tests that a room is successfully created
    def test_create_room_method(self):
        with patch("amity-app.rooms.room.Office"):
            self.amity.create_room("o", "uganda")
            self.assertIn("uganda", self.amity.offices['available'])
        with patch("amity-app.rooms.room.LivingSpace"):
            self.amity.create_room('l', 'kenya')
            self.assertIn('kenya', self.amity.living_spaces['available'])

    # tests that rooms number is increased by one after a room is added
    def test_create_room_increases_rooms_list_by_one(self):
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
    def test_living_space_can_only_be_created_once(self):
        with patch('amity-app.rooms.room.LivingSpace'):
            self.amity.create_room('l', 'php')
            db = self.amity.create_room('l', 'php')
            self.assertEqual(db, 'php already exists.')

    def test_office_can_only_be_created_once(self):
        pass

    def test_room_creation_when_successful(self):
        pass

    def test_returns_no_allocations_if_no_rooms_created(self):
        pass

    def test_returns_error_if_no_rooms_within_system(self):
        pass

    def test_validation_of_people_names(self):
        pass

    def test_validation_of_people_types(self):
        pass

    def test_wants_accomodation_is_either_y_or_n(self):
        pass

    def test_validation_if_person_fellow_and_wants_accomodation(self):
        pass

    def test_passes_validation_and_creates_person(self):
        pass

    def test_person_objects_are_created(self):
        pass

    def test_get_identifier_if_no_people_added(self):
        pass

    def test_get_identifier_if_people_added(self):
        pass

    def test_reallocate_person(self):
        pass

    def test_reallocate_person_when_room_does_not_exist(self):
        pass

    def test_reallocate_person_when_person_accomodate_is_N(self):
        pass

    def test_reallocate_to_same_room(self):
        pass

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
