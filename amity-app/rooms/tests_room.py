__author__ = 'scotty'


import unittest
from .room import LivingSpace, Office


class TestRoomClassFunctionality(unittest.TestCase):

    #
    def test_capacity(self):
        office = Office('red')
        ls = LivingSpace('reddish')
        self.assertEqual(office.capacity, 6)
        self.assertEqual(ls.capacity, 4)

    # Ls decrease by one when add person method is called
    def test_capacity_reduces_by_one_for_living_space(self):
        ls = LivingSpace('redddishh')
        self.assertEqual(ls.add_person('one'), 3)

    # O decrease by one when add person method is called
    def test_capacity_reduces_by_one_for_office(self):
        of = Office('reddd')
        self.assertEqual(of.add_person('one'), 5)
