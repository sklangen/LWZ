from lwz import *
from trf import *
from unittest import TestCase
import os
import tempfile

class SeasonTest(TestCase):
    maxDiff = None

    def test_load(self):
        path = os.path.join(os.path.dirname(__file__), 'test_season_directory_load_data')
        directory = SeasonDirectory(path)

        directory.load()

        season = directory.season
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

        self.assertEqual(set(directory.tournaments), {'Jun', 'Mar'})
        for tournament in directory.tournaments.values():
            self.assertIsInstance(tournament, Tournament)

        tour = directory.tournaments['Jun']
        self.assertEqual(len(tour.players), 13)
        self.assertEqual(tour.players[3].name, 'hansimpech')
        self.assertEqual(tour.players[6].points, 5.0)
        self.assertEqual(tour.players[12].games[3:], [Game(None, ' ', '-', i+1) for i in range(3, 10)])
        self.assertEqual(tour.players[2].games[3].result, '0')

    def test_dump(self):
        season_player = SeasonPlayer(
            id=123456789,
            dwz=666,
            stateOfMembership='GUEST',
            names=['Osh', 'Oshgnacknak', 'Osh Gnackank'],
        )

        season = Season(
            mode='BLITZ_5PLUS0',
            startYear=1337,
            players=[season_player]
        )

        player = Player(
            startrank=1,
            name='Oshgnacknak',
            sex='f',
            id=season_player.id,
            points=99.5,
            rating=9999,
            games=[Game((i+2)*2%1000, 'wbs- '[i%3], '1' or '10=+-wdlhfuz '[i%13], i+1) for i in range(5)],
        )

        tournament = Tournament(
            name='Oshgnacknak ist der Geilste, Open 2020',
            type='Osh gewinnt immer',
            xx_fields={'XXR': '33'},
            rounddates=['1618/05/23']*5,
            players=[player],
        )

        path = os.path.join(tempfile.gettempdir(), 'test_season_directory_dump_data') 
        os.makedirs(path, exist_ok=True)
        directory = SeasonDirectory(
            path, 
            season,
            tournaments={'Jan': tournament}
        )

        directory.dump()

        directory = SeasonDirectory(path)
        directory.load()

        self.assertEqual(directory.season, season)
        self.assertEqual(set(directory.tournaments), {'Jan'})

        tour = directory.tournaments['Jan']
        self.assertEqual(tour.rounddates, tournament.rounddates)
        self.assertEqual(tour, tournament)
