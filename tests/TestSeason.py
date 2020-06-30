from unittest import TestCase
from lwz import *
import os
import yaml

class SeasonTest(TestCase):

    def test(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'season.yml')

        player = SeasonPlayer(
            id='deadbeef',
            names=['Osh', 'Oshgnacknak', 'Osh Gnackank'],
            dwz=6789,
        )

        season = Season(
            mode='KIDS',
            startYear=2020,
            players=[player],
        )

        with open(filename, 'w') as f:
            yaml.dump(season, f, sort_keys=False)

        with open(filename) as f:
            season = yaml.load(f, Loader=yaml.Loader)

        self.assertIsInstance(season, Season)
        self.assertEqual(season.mode, 'KIDS')
        self.assertEqual(season.startYear, 2020)
        self.assertIsNone(season.parentSeason)
        self.assertEqual(len(season.players), 1)

        player = season.players[0]
        self.assertIsInstance(player, SeasonPlayer)
        self.assertEqual(player.id, 'deadbeef')
        self.assertEqual(player.names, ['Osh', 'Oshgnacknak', 'Osh Gnackank'])
        self.assertEqual(player.dwz, 6789)
        self.assertEqual(player.stateOfMembership, 'MEMBER')
