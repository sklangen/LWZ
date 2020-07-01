from unittest import TestCase
from lwz import *

class SeasonTest(TestCase):

    def test(self):
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

        path = os.path.join(os.path.dirname(__file__), 'data')
        directory = SeasonDirectory(path, season)

        directory.dump_season()
        season = directory.load_season()

        self.assertIsInstance(season, Season)
        self.assertEqual(season.mode, 'KIDS')
        self.assertEqual(season.startYear, 2020)
        self.assertEqual(season.endYear, 2021)
        self.assertIsNone(season.parentSeason)
        self.assertEqual(len(season.players), 1)

        player = season.players[0]
        self.assertIsInstance(player, SeasonPlayer)
        self.assertEqual(player.id, 'deadbeef')
        self.assertEqual(player.names, ['Osh', 'Oshgnacknak', 'Osh Gnackank'])
        self.assertEqual(player.dwz, 6789)
        self.assertEqual(player.stateOfMembership, 'MEMBER')
