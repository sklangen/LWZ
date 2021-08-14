from .utils import *
from csv import DictReader
import calendar
import trf


def query_lichess_ranks(tournament_id: str, tour: trf.Tournament):
    url = f'https://lichess.org/api/swiss/{tournament_id}/results'
    for json in http_get_ndjson(url):
        username = json['username'].lower()
        for player in tour.players:
            if player.name == username:
                player.rank = int(json['rank']) + 1
                break
        else:
            raise LWZException(f'No player for: {username}')


def parse_lichess(tournament_id: str) -> trf.Tournament:
    url = f'https://lichess.org/swiss/{tournament_id}.trf'
    content = http_get(url)
    tournament = trf.loads(content)
    month = tournament.startdate[:3]

    query_lichess_ranks(tournament_id, tournament)
    tournament.players.sort(key=lambda p: p.rank)

    return tournament, month


def parse_swiss(filename) -> trf.Tournament:
    with open(filename, encoding='ISO-8859-1') as f:
        tournament = trf.load(f)
    month = extract_month(tournament.startdate)
    return tournament, month


def extract_month(date: str) -> str:
    delim = '.'

    if '/' in date:
        delim = '/'

    return calendar.month_abbr[int(date.split(delim)[1])]


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
    return tournament, month


parsers = {
    'lichess': parse_lichess,
    'swiss': parse_swiss,
    'oldlwz': parse_oldlwz,
}
