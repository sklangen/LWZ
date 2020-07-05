from . import trf
from .utils import *
from csv import DictReader
import calendar


def parse_lichess(tournament_id: str) -> trf.Tournament:
    url = f'https://lichess.org/swiss/{tournament_id}.trf'
    content = http_get(url)
    tournament = trf.loads(content)
    return {
        'tournament': tournament,
        'month': tournament.startdate[:3],
        'rounds': int(tournament.xx_fields['XXR'])
    }


def parse_swiss(filename) -> trf.Tournament:
    with open(filename, encoding='ISO-8859-1') as f:
        tournament = trf.load(f)

    month = calendar.month_abbr[int(tournament.startdate.split('.')[1])]
    return {
        'tournament': tournament,
        'month': month
    }


def parse_oldlwz(filename) -> trf.Tournament:
    with open(filename) as f:
        players = [trf.Player(
            name=row['name'],
            startrank=i+1,
            rank=i+1,
            points=float(row['points']),
        ) for i, row in enumerate(DictReader(f))]
    
    tournament = trf.Tournament(
        name=filename,
        numplayers=len(players),
        players=players,
    )

    month = calendar.month_abbr[int(filename[-6:-4])]
    return {
        'tournament': tournament,
        'month': month,
        'rounds': len(players)-1,
    }


parsers = {
    'lichess': parse_lichess,
    'swiss': parse_swiss,
    'oldlwz': parse_oldlwz,
}
