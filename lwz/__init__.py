from .Season import Season, SeasonPlayer
from .trf import Tournament
from typing import Dict
import calendar
import os
import yaml

class SeasonDirectory:
    '''Collection of helper functions to save and load season information form a specified directory'''

    def __init__(self, path: str, season: Season=None, tournaments: Dict[str, Tournament]=None):
        self.path = path
        self.season = season
        self.tournaments = tournaments or {}

    def load_season(self) -> Season:
        '''Load season information from path/season.yml'''
        with open(self._season_yml_filename) as f:
            self.season = yaml.safe_load(f)
            return self.season

    def dump_season(self):
        '''Save season information into path/season.yml'''
        with open(self._season_yml_filename, 'w') as f:
            yaml.safe_dump(self.season, f, sort_keys=False)

    @property
    def _season_yml_filename(self) -> str:
        return os.path.join(self.path, 'season.yml')

    def load_tournament(self, month: str) -> Tournament:
        '''Load tournament from path/YYYY_MM.trf'''
        tournament = Tournament()
        tournament.parse(self._tournament_filename(month))
        self.tournaments[month] = tournament
        return tournament

    def dump_tournament(self, month: str):
        '''Save tournament into path/YYYY_MM.trf'''
        trf = self.tournaments[month].create_trf_file()
        with open(self._tournament_filename(month), 'w') as f:
            f.write(trf)

    def _tournament_filename(self, month: str) -> str:
        month = calendar.month_abbr.index(month)
        year = self.season.startYear if month > 4 else self.season.endYear
        return os.path.join(self.path, f'{year:04}_{month:02}.trf')

def init_season(directory, zps=None):
    logging.warn('Not gonna initialize!')

def import_tournament(directory, tournament, source, month, rounds=None, names=False):
    logging.warn('Not gonna import!')

def build_html(directory, seasons):
    logging.warn('Not gonna build!')
