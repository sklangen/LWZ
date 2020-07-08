from . import trf
from .utils import escape_umlaute
from dataclasses import dataclass, field
from typing import Dict, List, Iterable
import calendar
import os
import yaml


class MyYAMLObject(yaml.YAMLObject):
    @classmethod
    def _from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return cls(**data)
 
    @classmethod
    def _to_yaml(cls, dumper, data):
        return dumper.represent_mapping(cls._yaml_tag(), vars(data))

    @classmethod
    def _yaml_tag(cls):
        return u'!' + cls.__name__


@dataclass
class SeasonPlayer(MyYAMLObject):
    '''Represating a player participating in a season'''

    id: str
    firstname: str = None
    lastname: str = None
    dwz: int = 0
    stateOfMembership: str = 'MEMBER'
    names: List[str] = field(default_factory=list)
    
    @property
    def aliases(self) -> Iterable[str]:
        '''All aliases associated with this player'''
        for f in [str, escape_umlaute]:
            if not (self.firstname is None or self.lastname is None):
                yield f(self.firstname) + ' ' + f(self.lastname)
                yield f(self.lastname) + ', ' + f(self.firstname)
                yield f(self.lastname) + ',' + f(self.firstname)

            if self.firstname is not None:
                yield f(self.firstname)

            if self.lastname is not None:
                yield f(self.lastname)

        for name in self.names:
            yield name

        yield str(self.id)

    @property
    def name(self) -> str:
        '''Primary name of this player'''
        return next(self.aliases)

@dataclass
class Season(MyYAMLObject):
    '''Represating a season of monthly tournaments played from May, startYear to April, endYear'''

    mode: str
    startYear: int
    parentSeason: str = None
    players: List[SeasonPlayer] = field(default_factory=list)

    @property
    def name(self):
        return f'Saison {self.startYear}/{self.endYear-2000:02}'

    @property
    def endYear(self):
        return self.startYear+1


for cls in MyYAMLObject.__subclasses__():
    yaml.SafeDumper.add_multi_representer(cls, cls._to_yaml)
    yaml.SafeLoader.add_constructor(cls._yaml_tag(), cls._from_yaml)


class SeasonDirectory:
    '''Collection of helper functions to save and load season information from a specified directory'''

    def __init__(self, directory: str, season: Season=None, tournaments: Dict[str, trf.Tournament]=None):
        self.directory = directory
        self.season = season
        self.tournaments = tournaments or {}

    def load(self):
        '''Load all data from directory'''
        self.load_season()
        self.load_tournaments()

    def dump(self):
        '''Dump all data into directory'''
        self.dump_season()
        self.dump_tournaments()

    def add_player_by_name(self, name: str) -> SeasonPlayer:
        '''Create a player with that name, add it to the season and return it'''
        sp = SeasonPlayer(
            id=max((p.id for p in self.season.players if p.id < 10_000_000), default=0)+1,
            stateOfMembership='GUEST',
            names=[name]
        )
        self.season.players.append(sp)
        return sp

    def load_season(self):
        '''Load season information from directory/season.yml'''
        with open(self._season_yml_filename) as f:
            self.season = yaml.safe_load(f)

    def dump_season(self):
        '''Save season information into directory/season.yml'''
        with open(self._season_yml_filename, 'w') as f:
            yaml.safe_dump(self.season, f, sort_keys=False, allow_unicode=True)

    @property
    def _season_yml_filename(self) -> str:
        return os.path.join(self.directory, 'season.yml')

    def load_tournament(self, month: str):
        '''Load tournament from directory/YYYY_MM.trf.'''
        with open(self._tournament_filename(month)) as f:
            self.tournaments[month] = trf.load(f)

    def load_tournaments(self):
        '''Load all existing tournaments from directory/YYYY_MM.trf'''
        for month in calendar.month_abbr:
            if os.path.isfile(self._tournament_filename(month)):
                self.load_tournament(month)

    def dump_tournament(self, month: str):
        '''Save tournament into directory/YYYY_MM.trf'''
        with open(self._tournament_filename(month), 'w') as f:
            trf.dump(f, self.tournaments[month])

    def dump_tournaments(self):
        '''Save all tournaments into directory/YYYY_MM.trf'''
        for month in self.tournaments.keys():
            self.dump_tournament(month)

    def _tournament_filename(self, month: str) -> str:
        month = calendar.month_abbr[:].index(month)
        year = self.season.startYear if month > 4 else self.season.endYear
        return os.path.join(self.directory, f'{year:04}_{month:02}.trf')
