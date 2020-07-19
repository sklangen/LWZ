from . import trf
from .utils import escape_umlaute, LWZException
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Iterable, Tuple
import calendar
import itertools
import logging
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

    @property
    def is_dsb(self) -> str:
        '''Is this player listed on schachbund.de'''
        return self.id > 10_000_000

@dataclass
class Season(MyYAMLObject):
    '''Represating a season of monthly tournaments played from May, startYear to April, endYear'''

    mode: str
    startYear: int
    parentSeason: str = None
    players: List[SeasonPlayer] = field(default_factory=list)

    @property
    def name(self) -> str:
        return f'Saison {self.startYear}/{self.endYear-2000:02}'

    @property
    def outdir(self) -> str:
        return f'{self.mode.lower()}_{self.startYear-2000}{self.endYear-2000}'

    @property
    def startDate(self):
        return date(self.startYear, 5, 1)

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
        self.parentSeasonDir = None

    def load(self):
        '''Load all data from directory'''
        self.load_season()
        self.load_tournaments()

    def dump(self):
        '''Dump all data into directory'''
        self.dump_season()
        self.dump_tournaments()

    def load_season(self):
        '''Load season information from directory/season.yml'''
        with open(self._season_yml_filename) as f:
            self.season = yaml.safe_load(f)

        if self.season.parentSeason is not None:
            self.parentSeasonDir = SeasonDirectory(os.path.join(self.directory, self.season.parentSeason))
            self.parentSeasonDir.load_season()

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
        for month in calendar.month_abbr[1:]:
            if os.path.isfile(self._tournament_filename(month)):
                self.load_tournament(month)

        if self.parentSeasonDir is not None:
            self.parentSeasonDir.load_tournaments()

    def dump_tournament(self, month: str):
        '''Save tournament into directory/YYYY_MM.trf'''
        with open(self._tournament_filename(month), 'w') as f:
            trf.dump(f, self.tournaments[month])

    def dump_tournaments(self):
        '''Save all tournaments into directory/YYYY_MM.trf'''
        for month in self.tournaments.keys():
            self.dump_tournament(month)

    def _tournament_filename(self, month: str) -> str:
        return os.path.join(self.directory, self.as_date(month).strftime('%Y_%m.trf'))

    def as_date(self, month: str) -> date:
        month = calendar.month_abbr[:].index(month)
        year = self.season.endYear if month < 5 else self.season.startYear
        return date(year, month, 1)

    @property
    def all_players(self):
        '''Retuns all players in this season and all parent seasons'''
        if self.parentSeasonDir is not None:
            for p in self.parentSeasonDir.all_players:
                yield p

        for p in self.season.players:
            yield p

    def get_player_by_name(self, name: str) -> SeasonPlayer:
        '''Get our create a player associated with that name'''
        candidates = list(filter(lambda p: name in p.aliases, self.all_players))

        if len(candidates) != 1:
            raise LWZException(f'Number of candidates for name "{name}" not equal to one. Got: ' + str(candidates))

        return candidates[0]

    def add_player_by_name(self, name: str) -> SeasonPlayer:
        '''Create a player with that name, add it to the season and return it'''
        sp = SeasonPlayer(
            id=max((p.id for p in self.all_players if not p.is_dsb), default=0)+1,
            stateOfMembership='GUEST',
            names=[name]
        )
        self.season.players.append(sp)
        return sp

    def add_or_update_player(self, player: SeasonPlayer):
        '''If a player has this id, update id. Add it otherwise'''
        p = next(filter(lambda p: p.id == player.id, self.season.players), None)
        if p is not None:
            p.firstname = player.firstname
            p.lastname = player.lastname
            p.dwz = player.dwz
            p.stateOfMembership = player.stateOfMembership
        else:
            self.season.players.append(player)

    def months_played(self, player: SeasonPlayer) -> Iterable[Tuple[str, Tuple[trf.Player, trf.Tournament]]]:
        '''Returns the month name and the player of tournaments this SeasonPlayer took part in (including A-tournaments)'''
        if player.dwz < 1600 and self.parentSeasonDir is not None:
            for t in self.parentSeasonDir.months_played(player):
                yield t

        for m, t in self.tournaments.items():
            for p in t.players:
                if player.id == p.id:
                    yield m, (p, t)
