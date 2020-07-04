from dataclasses import dataclass, field
from typing import List, Dict
import io
import re


class TrfException(Exception):
    pass


@dataclass
class Round(object):
    startrank: int
    color: str
    result: str
    round: int


@dataclass
class Player(object):
    startrank: int
    name: str = ''
    sex: str = 'm'
    title: str = ''
    rating: int = 0
    fed: str = ''
    id: int = None
    birthdate: str = ''
    points: float = 0
    rank: int = None
    rounds: List[Round] = field(default_factory=list)


@dataclass
class Tournament(object):
    name: str = ''
    city: str = ''
    federation: str = ''
    startdate: str = ''
    enddate: str = ''
    numplayers: int = 0
    numratedplayers: int = 0
    numteams: int = 0
    type: str = ''
    chiefarbiter: str = ''
    deputyarbiters: str = ''
    rateofplay: str = ''
    rounddates: List[str] = field(default_factory=list) 
    players: List[Player] = field(default_factory=list) 
    teams: List[str] = field(default_factory=list) 
    xx_fields: Dict[str, str] = field(default_factory=dict)


def dump(fp, tournament):
    _dump_tournament(fp, tournament)


def dumps(tournament):
    fp = io.StringIO()
    _dump_tournament(fp, tournament)
    return fp.getvalue()


def _dump_tournament(fp, tournament):
    fp.write(f'012 {tournament.name}\n')
    fp.write(f'022 {tournament.city}\n')
    fp.write(f'032 {tournament.federation}\n')
    fp.write(f'042 {tournament.startdate}\n')
    fp.write(f'052 {tournament.enddate}\n')
    fp.write(f'062 {tournament.numplayers}\n')
    fp.write(f'072 {tournament.numratedplayers}\n')
    fp.write(f'082 {tournament.numteams}\n')
    fp.write(f'092 {tournament.type}\n')
    fp.write(f'102 {tournament.chiefarbiter}\n')
    fp.write(f'112 {tournament.deputyarbiters}\n')
    fp.write(f'122 {tournament.rateofplay}\n')
    fp.write(f'132 {" ".join(tournament.rounddates)}\n')

    for field, value in tournament.xx_fields.items():
        fp.write(f'{field} {value}\n')

    for player in tournament.players:
        _dump_player(fp, player)
        fp.write('\n')


def _dump_player(fp, player):
    fp.write('001')
    fp.write(f' {player.startrank:>4}')
    fp.write(f' {player.sex:1}')
    fp.write(f' {player.title:>2}')
    fp.write(f' {player.name:<33}')
    fp.write(f' {player.rating or "":>4}')
    fp.write(f' {player.fed:<3}')
    fp.write(f' {player.id or "":>11}')
    fp.write(f' {player.birthdate:>10}')
    fp.write(f' {player.points:>4}')
    fp.write(f' {"" if player.rank is None else player.rank:>4}')

    for round in player.rounds:
        fp.write(f'  {"0000" if round.startrank == 0 else round.startrank or "":>4} {round.color:1} {round.result:1}')


def load(fp):
    return _parse_tournament(fp.readlines())


def loads(s):
    return _parse_tournament(s.split('\n'))


def _parse_tournament(lines):
    tournament = Tournament()

    for line in lines:
        data = line[4:].strip()

        if line.startswith('012 '):
            tournament.name = data
        elif line.startswith('022 '):
            tournament.city = data
        elif line.startswith('032 '):
            tournament.federation = data
        elif line.startswith('042 '):
            tournament.startdate = data
        elif line.startswith('052 '):
            tournament.enddate = data
        elif line.startswith('062 '):
            tournament.numplayers = int(data)
        elif line.startswith('072 '):
            tournament.numratedplayers = int(data)
        elif line.startswith('082 '):
            tournament.numteams = int(data)
        elif line.startswith('092 '):
            tournament.type = data
        elif line.startswith('102 '):
            tournament.chiefarbiter = data
        elif line.startswith('112 '):
            tournament.deputyarbiters = data
        elif line.startswith('122 '):
            tournament.rateofplay = data
        elif line.startswith('132 '):
            tournament.rounddates = data.split()
        elif line.startswith('001 '):
            player = _parse_player(line)
            tournament.players.append(player)
        elif line.startswith('013 '):
            tournament.teams.append(data)
        elif line.startswith('XX'):
            name = line[:3]
            tournament.xx_fields[name] = data
    return tournament


_PLAYER_LINE_PATTERN = re.compile(r'^001 (?P<startrank>[ \d]{4}) (?P<sex>[\w ]) (?P<title>[\w ]{2}) (?P<name>.{33}) (?P<rating>[ \d]{4}) (?P<fed>[\w ]{3}) (?P<id>[ \d]{11}) (?P<birthdate>.{10}) (?P<points>[ \d.]{4}) (?P<rank>[ \d]{4})(?P<rounds>(  [ \d]{4} [bsw\- ] [1=0+wdl\-hfuz ]| {10})*)\s*$', re.IGNORECASE)
def _parse_player(line):
    match = _PLAYER_LINE_PATTERN.fullmatch(line)
    if match is None:
        raise TrfException('Line did not matching pattern: ' + line)

    return Player(
        startrank=int(match.group('startrank')),
        sex=match.group('sex'),
        title=match.group('title').strip(),
        name=match.group('name').strip(),
        rating=_int_or(match.group('rating'), 0),
        fed=match.group('fed').strip(),
        id=_int_or(match.group('id')),
        birthdate=match.group('birthdate').strip(),
        points=float(match.group('points')),
        rank=_int_or(match.group('rank')),
        rounds=list(_parse_rounds(match.group('rounds')[2:].rstrip())),
    )


def _parse_rounds(string):
    round = 1
    while len(string) >= 7:
        yield Round(
            startrank=_int_or(string[:4].strip()),
            color=string[5],
            result=string[7],
            round=round
        )
        round += 1
        string = string[10:]


def _int_or(string, default=None):
    if string == '' or string.isspace():
        return default
    return int(string)
