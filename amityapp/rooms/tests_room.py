__author__ = 'scotty'

import unittest
from room import LivingSpace, Office


class TestRoomClassFunctionality(unittest.TestCase):
    # tests that maximum for ls and O is 4 & 6
    def test_capacity(self):
        office = Office('red')
        ls = LivingSpace('reddish')
        self.assertEqual(office.capacity, 6)
        self.assertEqual(ls.capacity, 4)

    # Ls decrease by one when add person method is called
    def test_capacity_reduces_by_one_for_living_space(self):
        ls = LivingSpace('redddishh')
        self.assertEqual(ls.add_person('one'), 3)

    # Office decrease by one when add person method is called
    def test_capacity_reduces_by_one_for_office(self):
        of = Office('reddd')
        self.assertEqual(of.add_person('one'), 5)

    # tests whether room and type are used correctly when passing arguments for office
    def test_office_is_instance_of_class_Office(self):
        office = Office('green')
        self.assertEqual('Office', office.room_type)
        self.assertNotEqual('green', office.room_name)

    # tests whether room and type are used correctly when passing arguments for livingspace
    def test_living_space_is_instance_of_class_LivingSpace(self):
        ls = LivingSpace('greenish')
        self.assertEqual('Living Space', ls.room_type)
        self.assertNotEqual('greenish', ls.room_name)
