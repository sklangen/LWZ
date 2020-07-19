from datetime import date
from lwz.dewis import *
import unittest


class TestPastRatings(unittest.TestCase):

    def test_get_player_rating_at(self):
        ref_date = date(2018, 5, 1)
        r = get_player_rating_at(10562743, ref_date)
        self.assertIsInstance(r, int)
        self.assertEqual(r, 1684)

    def test_that_an_future_date_has_none_0_rating(self):
        ref_date = date(3018, 2, 15)
        r = get_player_rating_at(10029745, ref_date)
        self.assertIsInstance(r, int)
        self.assertNotEqual(r, 0)

    def test_no_tournaments_has_0_rating(self):
        ref_date = date(3018, 2, 15)
        r = get_player_rating_at(10583181, ref_date)
        self.assertIsInstance(r, int)
        self.assertEqual(r, 0)
