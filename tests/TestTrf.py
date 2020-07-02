from unittest import TestCase
from lwz import trf
import os

class SeasonTrt(TestCase):

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
        tour = trf.loads(trf_string)
        dumped = trf.dumps(tour)

        for i in range(100):
            for j, (acctual, expected) in enumerate(zip(dumped.split('\n'), trf_string.split('\n'))):
                self.assertEqual(acctual.strip(), expected.strip(), f'Diff in line {j+1}, iterration {i} of converting {filename} back and forth.')
        
            tour = trf.loads(dumped)
            dumped = trf.dumps(tour)
