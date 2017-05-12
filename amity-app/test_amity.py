__author__ = 'scotty'

import os

import unittest
from amity import Amity

from mock import patch


class TestAmityFunctionality(unittest.TestCase):
    def setUp(self):
        self.amity = Amity()

    def test_amity_class_initialises_with_nothing(self):
        self.assertEquals(len(self.amity.rooms), 0)
        self.assertEquals(len(self.amity.people), 0)
        self.assertEquals(len(self.amity.fellows), 0)
        self.assertEquals(len(self.amity.staff), 0)

    def test_returns_error_when_non_string_is_addded(self):
        pass

    def test_create_room_method(self):
        pass

    def test_create_room_increases_rooms_list_by_one(self):
        pass

    def test_living_space_can_only_be_created_once(self):
        pass

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
