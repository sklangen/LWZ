from .SeasonDirectory import SeasonPlayer
from .utils import int_or_default
from csv import DictReader
from io import StringIO
from typing import Iterable
from urllib.request import urlopen


class DewisException(Exception):
    pass


def get_club(zps: str) -> Iterable[SeasonPlayer]:
    url = 'https://www.schachbund.de/php/dewis/verein.php?format=csv&zps=' + zps
    resource = urlopen(url)
    content = resource.read().decode(resource.headers.get_content_charset())

    if content.startswith('Fehler: '):
        raise DewisException(content)

    f = StringIO(content)
    for row in DictReader(f, delimiter='|'):
        yield SeasonPlayer(
            id=int(row['id']),
            dwz=int_or_default(row['dwz'], 0),
            names=[row['vorname'] + ' ' + row['nachname']],
        )
