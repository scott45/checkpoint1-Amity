__author__ = 'scotty'

import unittest
from .person import Staff, Fellow


class TestPersonClass(unittest.TestCase):
    def test_Staff_person_label(self):
        s = Staff("taracha", "rogers")
        self.assertEqual(s.person_lable, "Staff")
