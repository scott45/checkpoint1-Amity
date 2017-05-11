__author__ = 'scotty'

import unittest
from .person import Staff, Fellow


class TestPersonClass(unittest.TestCase):
    def test_Fellow_two_names(self):
        pass

    def test_Staff_person_label(self):
        s = Staff("taracha", "rogers")
        self.assertEqual(s.person_label, "Staff")

    def test_Fellow_person_label(self):
        f = Fellow("scott", "businge")
        self.assertEqual(f.person_label, "Fellow")