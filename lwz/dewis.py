from .SeasonDirectory import SeasonPlayer
from .utils import *
from concurrent.futures import ThreadPoolExecutor 
from csv import DictReader
from io import StringIO
from typing import Iterable
import datetime
import logging
import lxml.html as lh
import math


class DewisException(Exception):
    pass


def _row_to_player(row):
    return SeasonPlayer(
        id=int(row['id']),
        dwz=int_or_default(row['dwz'], 0),
        firstname=row['vorname'],
        lastname=row['nachname'],
    )


def get_club(zps: str) -> Iterable[SeasonPlayer]:
    url = 'https://www.schachbund.de/php/dewis/verein.php?format=csv&zps=' + zps
    content = http_get(url)

    if content.startswith('Fehler: '):
        raise DewisException(content)

    f = StringIO(content)
    for row in DictReader(f, delimiter='|'):
        yield _row_to_player(row)


def get_player(pkz: int) -> SeasonPlayer:
    url = f'https://www.schachbund.de/php/dewis/spieler.php?pkz={pkz}&format=csv'
    content = http_get(url)

    if content.startswith('Fehler: '):
        raise DewisException(content)

    for row in DictReader(content.split('\n')[:2], delimiter='|'):
        return _row_to_player(row)


def get_participations(pkz: int) -> DictReader:
    url = f'https://www.schachbund.de/php/dewis/spieler.php?pkz={pkz}&format=csv'
    lines = http_get(url).split('\r\n')

    if lines[0].startswith('Fehler: '):
        raise DewisException(lines[0])

    index = lines.index('turniercode|turniername|dwzalt|dwzaltindex|punkte|partien|nichtgewertet|erwartungswert|gegner|koeffizient|dwzneu|dwzneuindex|leistung')
    return DictReader(lines[index:], delimiter='|')


def extract_date_from_tournament(tournament_id: str) -> datetime.date:
    if tournament_id == 'B053-000-DWZ':
        return datetime.date(2009, 1, 1)

    url = f'https://www.schachbund.de/turnier/{tournament_id}.html'
    doc = lh.fromstring(http_get(url))
    tr_elements = doc.xpath('//tr')

    for row in tr_elements:
        if not len(row) == 2:
            continue

        correct_row = False
        for el in row.iterchildren():
            if 'Erste Berechnung am:' in el.text_content():
                correct_row = True
                continue
            if correct_row:
                date_string = el.text_content().split(' ')[0]

                try:
                    return datetime.datetime.strptime(date_string, '%d.%m.%Y').date()
                except ValueError:
                    logging.warn(f'No valid date found for tournament id {tournament_id}. Got: ' + date_string)
                    return None


def get_player_rating_at(pkz: int, ref_date: datetime.date) -> int:
    participations = list(get_participations(pkz))

    if not participations:
        return 0

    with ThreadPoolExecutor(max_workers=4) as e:
        dates = e.map(lambda p: extract_date_from_tournament(p['turniercode']), participations)

    for participation, date in zip(participations, dates):
        if date is not None and date > ref_date:
            return int_or_default(participation['dwzalt'], 0)

    return int_or_default(participations[-1]['dwzneu'], 0)
