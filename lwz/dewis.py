from .SeasonDirectory import SeasonPlayer
from .utils import *
from csv import DictReader
from io import StringIO
from typing import Iterable



class DewisException(Exception):
    pass


def get_club(zps: str) -> Iterable[SeasonPlayer]:
    url = 'https://www.schachbund.de/php/dewis/verein.php?format=csv&zps=' + zps
    content = http_get(url)

    if content.startswith('Fehler: '):
        raise DewisException(content)

    f = StringIO(content)
    for row in DictReader(f, delimiter='|'):
        yield SeasonPlayer(
            id=int(row['id']),
            dwz=int_or_default(row['dwz'], 0),
            firstname=row['vorname'],
            lastname=row['nachname'],
        )
