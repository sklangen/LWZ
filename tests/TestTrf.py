from unittest import TestCase
from lwz import trf
import os

class SeasonTrt(TestCase):

    maxDiff = None

    def test_example1_chinese_whispers(self):
        self.chinese_whispers('example1')

    def test_2020_06_chinese_whispers(self):
        self.chinese_whispers('2020_06')

    def test_2021_03_chinese_whispers(self):
        self.chinese_whispers('2021_03')

    def chinese_whispers(self, name):
        filename = os.path.join(os.path.dirname(__file__), 'test_trf_chinese_whispers', name+'.trf')

        with open(filename) as f:
            trf_string = f.read()
        tour0 = trf.loads(trf_string)
        dumped = trf.dumps(tour0)

        for i in range(100):
            itertext = f' in iteration {i+1}'

            for j, (acctual, expected) in enumerate(zip(dumped.split('\n'), trf_string.split('\n'))):
                self.assertEqual(acctual.strip(), expected.strip(), f'Diff of line {j+1}' + itertext)

            tour = trf.loads(dumped)
            dumped = trf.dumps(tour)

            self.assertEqual(tour.name, tour0.name, f'Diff of {{tournament.name}}' + itertext)
            self.assertEqual(tour.city, tour0.city, f'Diff of {{tournament.city}}' + itertext)
            self.assertEqual(tour.federation, tour0.federation, f'Diff of {{tournament.federation}}' + itertext)
            self.assertEqual(tour.startdate, tour0.startdate, f'Diff of {{tournament.startdate}}' + itertext)
            self.assertEqual(tour.enddate, tour0.enddate, f'Diff of {{tournament.enddate}}' + itertext)
            self.assertEqual(tour.numplayers, tour0.numplayers, f'Diff of {{tournament.numplayers}}' + itertext)
            self.assertEqual(tour.numratedplayers, tour0.numratedplayers, f'Diff of {{tournament.numratedplayers}}' + itertext)
            self.assertEqual(tour.numteams, tour0.numteams, f'Diff of {{tournament.numteams}}' + itertext)
            self.assertEqual(tour.type, tour0.type, f'Diff of {{tournament.type}}' + itertext)
            self.assertEqual(tour.chiefarbiter, tour0.chiefarbiter, f'Diff of {{tournament.chiefarbiter}}' + itertext)
            self.assertEqual(tour.deputyarbiters, tour0.deputyarbiters, f'Diff of {{tournament.deputyarbiters}}' + itertext)
            self.assertEqual(tour.rateofplay, tour0.rateofplay, f'Diff of {{tournament.rateofplay}}' + itertext)
            self.assertEqual(tour.rounddates, tour0.rounddates, f'Diff of {{tournament.rounddates}}' + itertext)
            self.assertEqual(tour.xx_fields, tour0.xx_fields, f'Diff of {{tournament.xx_fields}}' + itertext)

            for j, (player, player0) in enumerate(zip(tour.players, tour0.players)):
                self.assertEqual(player.startrank, player0.startrank, f'Diff of {{player[{j}].startrank}}' + itertext)
                self.assertEqual(player.sex, player0.sex, f'Diff of {{player[{j}].sex}}' + itertext)
                self.assertEqual(player.title, player0.title, f'Diff of {{player[{j}].title}}' + itertext)
                self.assertEqual(player.name, player0.name, f'Diff of {{player[{j}].name}}' + itertext)
                self.assertEqual(player.rating, player0.rating, f'Diff of {{player[{j}].rating}}' + itertext)
                self.assertEqual(player.fed, player0.fed, f'Diff of {{player[{j}].fed}}' + itertext)
                self.assertEqual(player.id, player0.id, f'Diff of {{player[{j}].id}}' + itertext)
                self.assertEqual(player.birthdate, player0.birthdate, f'Diff of {{player[{j}].birthdate}}' + itertext)
                self.assertEqual(player.points, player0.points, f'Diff of {{player[{j}].points}}' + itertext)
                self.assertEqual(player.rank, player0.rank, f'Diff of {{player[{j}].rank}}' + itertext)
